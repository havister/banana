from django.urls import path
from events import views

app_name = 'events'

urlpatterns = [
    # /events/study/
    path('study/', views.StudyView.as_view(), name='study'),
    # /events/study/apply/
    path('study/apply/', views.StudyApplyView.as_view(), name='study_apply'),
    # /events/study/thanks/
    path('study/thanks/', views.StudyThanksView.as_view(), name='study_thanks'),
]
