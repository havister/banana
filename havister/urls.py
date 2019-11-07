from django.urls import path
from havister import views

app_name = 'havister'

urlpatterns = [
    # /havister/
    path('', views.IndexView.as_view(), name='index'),
    # /havister/v1/operation/
    path('v1/operation/', views.operation, name='operation'),
    # /havister/v1/<username>/account/
    path('v1/<username>/account/', views.account, name='account'),
    # /havister/v1/<username>/signals/
    path('v1/<username>/signals/', views.signals, name='signals'),
    # /havister/v1/<username>/log/
    #path('v1/<username>/log/', views.account, name='log'),
    # /havister/v1/<username>/trade/
    #path('v1/<username>/trade/', views.account, name='trade'),
]
