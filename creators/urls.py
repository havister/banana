from django.urls import path
from creators.views import IndexView

app_name = 'creators'

urlpatterns = [
    # /creators/
    path('', IndexView.as_view(), name='index'),
]
