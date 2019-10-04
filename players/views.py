from django.views.generic import TemplateView
from django.contrib.auth.models import User
from trades.models import Trade


class IndexView(TemplateView):
    template_name = 'players/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Closed trade list by player
        context['player_trade_list'] = Trade.objects.filter(
            date_closed__isnull=False).order_by('player', '-date_closed').distinct('player')
        # New player list
        context['new_player_list'] = User.objects.filter(
            groups__name='player', trade=None).order_by('-date_joined')
        return context
