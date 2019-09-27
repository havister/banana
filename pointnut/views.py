from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from trades.models import Trade


def login_redirect(request):
    return redirect('user', request.user.username)


def password_change_done(request):
    return redirect('user', request.user.username)


class IndexView(TemplateView):
    template_name = 'index.html'


class UserView(LoginRequiredMixin, TemplateView):
    template_name = 'user.html'
    
    def get(self, request, *args, **kwargs):
        if request.user.username != kwargs['user']:
            return redirect('/')
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # User
        user = self.request.user
        context['user'] = user
        # Opened trade list
        context['opened_trade_list'] = Trade.objects.filter(
            player=user, date_closed__isnull=True).order_by('-date_opened')[:5]
        # Closed trade list
        context['closed_trade_list'] = Trade.objects.filter(
            player=user, date_closed__isnull=False).order_by('-date_closed')[:5]
        return context
    