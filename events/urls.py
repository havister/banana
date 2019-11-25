from django.urls import path
from events import views

app_name = 'events'

urlpatterns = [
    # /events/launch/
    #path('launch/', views.LaunchView.as_view(), name='launch'),
    # /events/launch/apply/
    #path('launch/apply/', views.LaunchApplyView.as_view(), name='launch_apply'),
    # /events/launch/thanks/
    #path('launch/thanks/', views.LaunchThanksView.as_view(), name='launch_thanks'),
    # /events/launch/notice/
    #path('launch/notice/', views.LaunchNoticeView.as_view(), name='launch_notice'),
    # /events/study/
    path('study/', views.StudyView.as_view(), name='study'),
]
