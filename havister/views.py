from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from pointnut.commons import ChoiceInfo
from havister.models import Log
from markets.models import SpecialDay
from strategies.models import Signal
from players.models import Play, Trade
from decimal import Decimal, ROUND_HALF_UP
import json


class IndexView(TemplateView):
    template_name = 'havister/index.html'


def run(request):
    # Today
    date = timezone.now().date()
    today = SpecialDay.objects.filter(date=date, is_active=True).first()
    if today is None:
        is_holiday = False
        start_time = "09:00:00"
        end_time = "15:20:00"
    else:
        is_holiday = today.is_holiday
        start_time = today.start_time
        end_time = today.end_time
    # Today data
    data = {
        'Date': date,
        'IsHoliday': is_holiday,
        'StartTime': start_time,
        'EndTime': end_time
    }
    return JsonResponse(data, safe=False)


@csrf_exempt
def account(request):
    data = {}
    if request.method == 'POST':
        # JSON
        json_data = json.loads(request.body.decode('utf-8'))
        player = User.objects.filter(username=json_data['Player']).first()
        account = player.account
        # Account data
        data = account.as_json_dict
    return JsonResponse(data, safe=False)


@csrf_exempt
def signals(request):
    data = []
    if request.method == 'POST':
        # JSON
        json_data = json.loads(request.body.decode('utf-8'))
        player = User.objects.filter(username=json_data['Player']).first()
        plays = player.plays.filter(date_unbound__isnull=True).order_by('date_bound')

        for play in plays:
            # Signal
            signal = play.signal
            signal_data = signal.as_json_dict

            # Watch list
            today = timezone.now().date()
            watches = signal.watches.filter(
                date_started__lte=today,
                date_touched__isnull=True,
                is_active=True
            ).order_by('date_updated')

            # Signal <- Watch list
            signal_data['Watches'] = []
            for watch in watches:
                watch_data = watch.as_json_dict
                signal_data['Watches'].append(watch_data)
                
                # Order list
                close_orders = watch.orders.filter(status_choice='C', is_active=True). \
                    order_by('position_choice')
                open_orders = watch.orders.filter(status_choice='O', is_active=True). \
                    order_by('position_choice')

                # Watch <- Close order list
                watch_data['CloseOrders'] = []
                for order in close_orders:
                    trade = Trade.objects.filter(
                        player=player,
                        signal=order.watch.signal,
                        level=order.level,
                        position_choice=order.position_choice,
                        piece=order.piece,
                        date_closed__isnull=True
                    ).order_by('-date_opened').first()
                    if trade:
                        close_data = order.as_json_dict
                        watch_data['CloseOrders'].append(close_data)
                # Watch <- Open order list
                watch_data['OpenOrders'] = []
                for order in open_orders:
                    trade = Trade.objects.filter(
                        player=player,
                        signal=order.watch.signal,
                        level=order.level,
                        position_choice=order.position_choice,
                        piece=order.piece,
                        date_closed__isnull=True
                    ).order_by('-date_opened').first()
                    if not trade:
                        open_data = order.as_json_dict
                        watch_data['OpenOrders'].append(open_data)
            # Signal data
            data.append(signal_data)
    return JsonResponse(data, safe=False)


@csrf_exempt
def message(request):
    if request.method == 'POST':
        # JSON
        json_data = json.loads(request.body.decode('utf-8'))
        player = User.objects.filter(username=json_data['Player']).first()
        message = json_data['Message']
        code = json_data['Code']
        datetime = json_data['Datetime']
        # Log Create
        Log.objects.create(
            player=player, message=message, code=code, datetime=datetime
        )
    return HttpResponse('OK')


@csrf_exempt
def trades(request):
    if request.method == 'POST':
        # JSON
        json_data = json.loads(request.body.decode('utf-8'))
        player = User.objects.filter(username=json_data['Player']).first()
        signal = Signal.objects.filter(pk=json_data['SignalPk']).first()
        
        # Close trade list
        for close_trade in json_data['CloseTrades']:
            trade = Trade.objects.filter(
                player=player,
                signal=signal,
                level=close_trade['Level'],
                position_choice=close_trade['PositionChoice'],
                piece=close_trade['Piece'],
                date_closed__isnull=True
            ).order_by('-date_opened').first()
            
            # Price
            price_opened = trade.price_opened
            price_closed = Decimal(close_trade['PriceClosed'])
            difference = Decimal(0)
            if signal.is_index or trade.position_choice == ChoiceInfo.LONG:
                difference = price_closed - price_opened
            else:
                difference = price_opened - price_closed
            change = (difference / price_opened * 100).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)

            # Trade update
            trade.price_closed = price_closed
            trade.difference = difference
            trade.change = change
            trade.date_closed = close_trade['DateClosed']
            trade.save()
            
        # Open trade list
        for trade in json_data['OpenTrades']:
            # Trade create
            Trade.objects.create(
                player=player, signal=signal,
                level=trade['Level'], position_choice=trade['PositionChoice'], piece=trade['Piece'],
                quantity=trade['Quantity'], price_opened=trade['PriceOpened'], date_opened=trade['DateOpened']
            )
    return HttpResponse('OK')
