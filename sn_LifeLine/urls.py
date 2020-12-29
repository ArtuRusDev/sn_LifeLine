"""sn_LifeLine URL Configuration

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
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

import mainapp
import messengerapp.views as messengerapp
from mainapp.views import main_page
from sn_LifeLine import settings

urlpatterns = [
    path('django_admin_panel/', admin.site.urls, name='admin'),
    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    path('', main_page, name='main'),
    path('news/', include('newsapp.urls', namespace='news')),
    path('profile/', include('profileapp.urls', namespace='profile')),
    path('users/', include('authapp.urls', namespace='auth')),
    path('friends/', include('friendsapp.urls', namespace='friends')),
    path('dialogs/', include('messengerapp.urls', namespace='messenger')),

]

handler404 = mainapp.views.handler404

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
