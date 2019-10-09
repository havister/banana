from django.urls import path
from users import views

app_name = 'users'

urlpatterns = [
    # /users/
    path('', views.IndexView.as_view(), name='index'),
    # /users/havister/
    #path('havister/', views.HavisterView.as_view(), name='havister'),
    # /users/trades/closed/
    path('trades/closed/', views.ClosedView.as_view(), name='trades_closed'),
    # /users/trades/opened/
    path('trades/opened/', views.OpenedView.as_view(), name='trades_opened'),
]
