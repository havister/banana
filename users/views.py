from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from players.models import Account, Trade


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'users/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        # Account
        context['account'] = Account.objects.filter(player=user).first()
        # Closed trade list
        context['closed_trade_list'] = Trade.objects.filter(
            player=user, date_closed__isnull=False).order_by('-date_closed')[:5]
        # Opened trade list
        context['opened_trade_list'] = Trade.objects.filter(
            player=user, date_closed__isnull=True).order_by('-date_opened')[:5]
        return context


class ClosedView(LoginRequiredMixin, TemplateView):
    template_name = 'users/closed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        # Closed trade list
        context['trade_list'] = Trade.objects.filter(
            player=user, date_closed__isnull=False).order_by('-date_closed')
        return context


class OpenedView(LoginRequiredMixin, TemplateView):
    template_name = 'users/opened.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        # Opened trade list
        context['trade_list'] = Trade.objects.filter(
            player=user, date_closed__isnull=True).order_by('-date_opened')
        return context
