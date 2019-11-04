from django.urls import path
from users import views

app_name = 'users'

urlpatterns = [
    # /users/
    path('', views.IndexView.as_view(), name='index'),
    # /users/strategy/
    path('strategy/', views.StrategyView.as_view(), name='strategy'),
    # /users/strategy/add/
    path('strategy/add/', views.StrategyAddView.as_view(), name='strategy_add'),
    # /users/strategy/add/done/
    path('strategy/add/done/', views.StrategyAddDoneView.as_view(), name='strategy_add_done'),
    # /users/signal/
    path('signal/', views.SignalView.as_view(), name='signal'),
    # /users/signal/<pk>/
    path('signal/<int:pk>/', views.SignalDetailView.as_view(), name='signal_detail'),
    # /users/signal/add/
    path('signal/add/', views.SignalAddView.as_view(), name='signal_add'),
    # /users/signal/add/done/
    path('signal/add/done/', views.SignalAddDoneView.as_view(), name='signal_add_done'),
    # /users/havister/
    path('havister/', views.HavisterView.as_view(), name='havister'),
    # /users/trades/closed/
    path('trades/closed/', views.ClosedView.as_view(), name='trades_closed'),
    # /users/trades/opened/
    path('trades/opened/', views.OpenedView.as_view(), name='trades_opened'),
]
