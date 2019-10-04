from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from trades.models import Trade


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'users/index.html'
    
    def dispatch(self, request, *args, **kwargs):
        username = request.user.username
        if kwargs['username'] != username:
            return redirect('users:index', username)
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        # Opened trade list
        context['opened_trade_list'] = Trade.objects.filter(
            player=user, date_closed__isnull=True).order_by('-date_opened')[:5]
        # Closed trade list
        context['closed_trade_list'] = Trade.objects.filter(
            player=user, date_closed__isnull=False).order_by('-date_closed')[:5]
        return context


class ReturnsView(LoginRequiredMixin, TemplateView):
    template_name = 'users/returns.html'

    def dispatch(self, request, *args, **kwargs):
        username = request.user.username
        if kwargs['username'] != username:
            return redirect('users:returns', username)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        # Closed trade list
        context['trade_list'] = Trade.objects.filter(
            player=user, date_closed__isnull=False).order_by('-date_closed')
        return context
