from django.urls import path
from signals.views import IndexView

app_name = 'signals'

urlpatterns = [
    # /signals/
    path('', IndexView.as_view(), name='index'),
]
