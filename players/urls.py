from django.urls import path
from players import views

app_name = 'players'

urlpatterns = [
    # /players/
    path('', views.IndexView.as_view(), name='index'),
]
