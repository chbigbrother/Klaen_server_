"""myserver URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.urls import path, include
from scheduler.views import *
from .views import *
from account.views import login
urlpatterns = [
    path('admin/', admin.site.urls),
    path('get/airquality/', get_busan_air_qualily),
    path('post/airquality/', post_air_quality),
    path('account/', include('account.urls')),
    path('scheduler/', include('scheduler.urls')),
    path('sensor/', include('sensor.urls')),
    path('menu/', include('menu.urls')),
    path('', login),
    path('home/', home),
]
urlpatterns += staticfiles_urlpatterns()
