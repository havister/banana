from django.urls import path
from strategies.views import IndexView

app_name = 'strategies'

urlpatterns = [
    # /strategies/
    path('', IndexView.as_view(), name='index'),
]
