"""pointnut URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from pointnut import views

urlpatterns = [
    # www.pointnut.com/
    path('', views.IndexView.as_view(), name='index'),
    # /admin/
    path('admin/', admin.site.urls),

    # /accounts/login/redirect/
    path('accounts/login/redirect/', views.login_redirect, name='login_redirect'),
    # /accounts/reset/done/
    path('accounts/reset/done/', views.password_reset_complete, name='password_reset_complete'),
    # /accounts/
    path('accounts/', include('django.contrib.auth.urls')),
    
    # /creators/
    path('creators/', include('creators.urls')),
    # /events/
    path('events/', include('events.urls')),
    # /havister/
    path('havister/', include('havister.urls')),
    # /players/
    path('players/', include('players.urls')),
    # /signals/
    path('signals/', include('signals.urls')),
    
    # /USER/
    path('<username>/', views.UserView.as_view(), name='user_index'),
]
