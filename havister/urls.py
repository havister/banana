from django.urls import path
from havister.views import IndexView

app_name = 'havister'

urlpatterns = [
    # /havister/
    path('', IndexView.as_view(), name='index'),
]
