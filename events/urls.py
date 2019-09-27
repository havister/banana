from django.urls import path
from events.views import IndexView

app_name = 'events'

urlpatterns = [
    # /events/
    path('', IndexView.as_view(), name='index'),
]
