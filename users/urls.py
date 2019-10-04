from django.urls import path
from users import views

app_name = 'users'

urlpatterns = [
    # /users/USER/
    path('<username>/', views.IndexView.as_view(), name='index'),
    # /users/USER/returns/
    path('<username>/returns/', views.ReturnsView.as_view(), name='returns'),
]
