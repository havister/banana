from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from strategies.models import Strategy, Signal


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'users/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        # Closed trade list
        context['closed_trade_list'] = user.trades.filter(
            date_closed__isnull=False).order_by('-date_closed')[:3]
        # Opened trade list
        context['opened_trade_list'] = user.trades.filter(
            date_closed__isnull=True).order_by('-date_opened')[:3]
        return context


class StrategyView(LoginRequiredMixin, TemplateView):
    template_name = 'users/strategy.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        # Basket list
        context['basket_list'] = user.baskets.filter(is_active=True).order_by('-date_bound')
        return context


class StrategyAddView(LoginRequiredMixin, TemplateView):
    template_name = 'users/strategy_add.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        # Strategy list
        strategies = Strategy.objects.filter(is_active=True).order_by('date_created')
        context['strategy_list'] = strategies
        return context


class SignalView(LoginRequiredMixin, TemplateView):
    template_name = 'users/signal.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        # Play list
        context['play_list'] = user.plays.filter(is_active=True).order_by('-date_bound')
        return context


class SignalAddView(LoginRequiredMixin, TemplateView):
    template_name = 'users/signal_add.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        # Signal list
        signals = Signal.objects.filter(is_active=True).order_by('date_created')
        context['signal_list'] = signals
        return context


class HavisterView(LoginRequiredMixin, TemplateView):
    template_name = 'users/havister.html'


class ClosedView(LoginRequiredMixin, TemplateView):
    template_name = 'users/closed_trade_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        # Closed trade list
        context['trade_list'] = user.trades.filter(
            date_closed__isnull=False).order_by('-date_closed')
        return context


class OpenedView(LoginRequiredMixin, TemplateView):
    template_name = 'users/opened_trade_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        # Opened trade list
        context['trade_list'] = user.trades.filter(
            date_closed__isnull=True).order_by('-date_opened')
        return context
