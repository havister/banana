from django.urls import path
from users import views

app_name = 'users'

urlpatterns = [
    # /users/
    path('', views.IndexView.as_view(), name='index'),
    # /users/returns/
    path('returns/', views.ReturnsView.as_view(), name='returns'),
]
