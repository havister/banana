from django.urls import path
from events import views

app_name = 'events'

urlpatterns = [
    # /events/
    path('', views.IndexView.as_view(), name='index'),
    # /events/launch/
    path('launch/', views.LaunchView.as_view(), name='launch'),
    # /events/launch/thanks/
    path('launch/thanks/', views.ThanksView.as_view(), name='thanks'),
    # /events/launch/notice/
    path('launch/notice/', views.NoticeView.as_view(), name='notice'),
]
