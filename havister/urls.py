from django.urls import path
from havister import views

app_name = 'havister'

urlpatterns = [
    # /havister/
    path('', views.IndexView.as_view(), name='index'),
    # /havister/v1/market/
    path('v1/market/', views.market, name='market'),
    # /havister/v1/account/
    path('v1/account/', views.account, name='account'),
    # /havister/v1/signals/
    path('v1/signals/', views.signals, name='signals'),
    # /havister/v1/message/
    path('v1/message/', views.message, name='message'),
    # /havister/v1/trades/
    path('v1/trades/', views.trades, name='trades'),
]
