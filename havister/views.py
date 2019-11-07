from django.utils import timezone
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.generic import TemplateView
from markets.models import SpecialDay
from players.models import Play


class IndexView(TemplateView):
    template_name = 'havister/index.html'


def operation(request):
    # Today
    date = timezone.now().date()
    today = Operation.objects.filter(date=date, is_active=True).first()
    if today is None:
        is_holiday = False
        start_time = "09:00:00"
        end_time = "15:20:00"
    else:
        is_holiday = today.is_holiday
        start_time = today.start_time
        end_time = today.end_time
    # Today data
    data = [{
        'date': date,
        'is_holiday': is_holiday,
        'start_time': start_time,
        'end_time': end_time
    }]
    return JsonResponse(data, safe=False)


def account(request, username):
    # Player
    user = User.objects.filter(username=username).first()
    account = user.account
    # Account data
    data = [{
        'player': username,
        'primary_budget': account.primary_budget,
        'secondary_budget': account.secondary_budget,
        'is_real': account.is_real,
        'has_havister': account.has_havister,
        'is_active': account.is_active
    }]
    return JsonResponse(data, safe=False)


def signals(request, username):
    # Player
    user = User.objects.filter(username=username).first()
    plays = user.plays.filter(date_unbound__isnull=True).order_by('date_bound')

    data = []
    for play in plays:
        # Signal
        signal = play.signal
        signal_data = {
            'strategy': signal.strategy.name,
            'asset': signal.asset,
            'long_item': signal.long_item,
            'short_item': signal.short_item,
            'unit_amount': signal.unit_amount
        }
        # Watch list
        today = timezone.now().date()
        watches = signal.watches.filter(
            date_started__lte=today,
            date_touched__isnull=True,
            is_active=True
        ).order_by('date_updated')
        # Signal - Watch list
        signal_data['watches'] = []
        for watch in watches:
            watch_data = {
                'price': watch.price,
                'condition': watch.condition,
                'start_time': watch.start_time,
                'end_time': watch.end_time,
            }
            signal_data['watches'].append(watch_data)
            # Order list
            open_orders = watch.orders.filter(status_choice='O', is_active=True). \
                order_by('position_choice')
            close_orders = watch.orders.filter(status_choice='C', is_active=True). \
                order_by('position_choice')
            # Watch - Open order list
            watch_data['open_orders'] = []
            for order in open_orders:
                open_data = {
                    'level': order.level,
                    'position': order.position,
                    'piece': order.piece,
                    'status': order.status,
                    'order': order.order
                }
                watch_data['open_orders'].append(open_data)
            # Watch - Close order list
            watch_data['close_orders'] = []
            for order in close_orders:
                close_data = {
                    'level': order.level,
                    'position': order.position,
                    'piece': order.piece,
                    'status': order.status,
                    'order': order.order
                }                
                watch_data['close_orders'].append(close_data)
        # Signal data
        data.append(signal_data)
    return JsonResponse(data, safe=False)
