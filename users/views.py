from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView, View
from django.db.models import Subquery, Sum
from markets.models import Market
from strategies.models import Strategy, Signal
from players.models import Shopping, Play
import datetime


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'users/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        # Group
        group = user.groups.filter(name__in=['player', 'observer']).first()
        context['group'] = group
        # Closed trade list
        context['closed_trade_list'] = user.trades.filter(date_closed__isnull=False). \
            order_by('-date_closed')[:3]
        # Opened trade list
        context['opened_trade_list'] = user.trades.filter(date_closed__isnull=True). \
            order_by('-date_opened')[:3]
        return context


class StrategyView(LoginRequiredMixin, TemplateView):
    template_name = 'users/strategy.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        # Shopping list
        context['shopping_list'] = user.shoppings.filter(date_unbound__isnull=True). \
            order_by('-date_bound')
        return context


class StrategyAddView(LoginRequiredMixin, TemplateView):
    template_name = 'users/strategy_add.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        shoppings = user.shoppings.filter(date_unbound__isnull=True)
        # Strategy list
        context['strategy_list'] = Strategy.objects.filter(is_active=True). \
            exclude(pk__in=Subquery(shoppings.values('strategy'))). \
            order_by('name')
        return context


class StrategyAddDoneView(LoginRequiredMixin, View):
    def post(self, request,*args, **kwargs):
        user = request.user
        strategy_id = request.POST['strategy_id']
        strategy = Strategy.objects.filter(id=strategy_id).first()
        # Strategy add
        if strategy:
            Shopping.objects.create(player=user, strategy=strategy)
        return redirect('users:strategy')


class SignalView(LoginRequiredMixin, TemplateView):
    template_name = 'users/signal.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        # Play list
        context['play_list'] = user.plays.filter(date_unbound__isnull=True). \
            order_by('-date_bound')
        return context


class SignalDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'users/signal_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        # Signal
        signal = get_object_or_404(Signal, pk=context['pk'])
        context['signal'] = signal
        # Watch list
        watch_list = []
        watches = signal.watches.filter(date_touched__isnull=True, is_active=True). \
            order_by('-date_updated')
        for watch in watches:
            # Order list
            open_orders = watch.orders.filter(status_choice='O', is_active=True). \
                order_by('position_choice')
            close_orders = watch.orders.filter(status_choice='C', is_active=True). \
                order_by('position_choice')
            watch_list.append({'item': watch, 'open_orders': open_orders, 'close_orders': close_orders})
        context['watch_list'] = watch_list
        return context


class SignalAddView(LoginRequiredMixin, TemplateView):
    template_name = 'users/signal_add.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        plays = user.plays.filter(date_unbound__isnull=True)
        shoppings = user.shoppings.filter(date_unbound__isnull=True)
        # Budget
        context['budget'] = user.account.primary_budget
        context['budget_used'] = plays.aggregate(sum=Sum('signal__total_amount'))['sum'] or 0
        context['budget_unused'] = context['budget'] - context['budget_used']
        # Signal list
        context['signal_list'] = Signal.objects. \
            filter(strategy__in=Subquery(shoppings.values('strategy')), is_active=True). \
            exclude(pk__in=Subquery(plays.values('signal'))). \
            order_by('strategy')
        return context


class SignalAddDoneView(LoginRequiredMixin, View):
    def post(self, request,*args, **kwargs):
        user = request.user
        signal_id = request.POST['signal_id']
        signal = Signal.objects.filter(id=signal_id).first()
        # Signal add
        if signal:
            Play.objects.create(player=user, signal=signal)
        return redirect('users:signal')


class HavisterView(LoginRequiredMixin, TemplateView):
    template_name = 'users/havister.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        # Market time
        start_time = datetime.time(9, 0)
        end_time = datetime.time(15, 45)
        # Today
        now = timezone.now()
        today = now.date()
        time = now.time()
        messages = user.messages.filter(datetime__date=today).order_by('pk')
        market = Market.objects.filter(date=today, is_active=True).first()
        # Messages
        message_list = []
        if messages:
            for message in messages:
                message_list.append(message.time_str)
        else:
            if today.weekday() >= 5: # 5-Saturday, 6-Sunday
                message_list.append("오늘은 휴장일 입니다.")
            if market:
                if market.is_holiday:
                    message_list.append("오늘은 휴장일 입니다.")
            if len(message_list) == 0:
                message_list.append("하비스터가 준비 중 입니다.")
                if time >= start_time:
                    message_list.append(start_time.strftime('%H:%M:%S') + " | 하비스터가 시장을 감시 중 입니다.")
                if time > end_time:
                    message_list.append(end_time.strftime('%H:%M:%S') + " | 시장이 마감 되었습니다.")
                    message_list.append("하비스터가 종료 되었습니다.")
        context['message_list'] = message_list
        # Closed trade list
        context['closed_trade_list'] = user.trades.filter(date_closed__date=today). \
            order_by('-date_closed')
        # Opened trade list
        context['opened_trade_list'] = user.trades.filter(date_opened__date=today, date_closed__isnull=True). \
            order_by('-date_opened')
        return context


class ClosedView(LoginRequiredMixin, TemplateView):
    template_name = 'users/closed_trade_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        # Closed trade list
        context['trade_list'] = user.trades.filter(date_closed__isnull=False). \
            order_by('-date_closed')
        return context


class OpenedView(LoginRequiredMixin, TemplateView):
    template_name = 'users/opened_trade_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        # Opened trade list
        context['trade_list'] = user.trades.filter(date_closed__isnull=True). \
            order_by('-date_opened')
        return context
