# sn_LifeLine URL Configuration
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path

import mainapp
from mainapp.views import main_page
from sn_LifeLine import settings

urlpatterns = [
    path('', main_page, name='main'),
    path('news/', include('newsapp.urls', namespace='news')),
    path('profile/', include('profileapp.urls', namespace='profile')),
    path('users/', include('authapp.urls', namespace='auth')),
    path('friends/', include('friendsapp.urls', namespace='friends')),
    path('dialogs/', include('messengerapp.urls', namespace='messenger')),
    path('community/', include('communityapp.urls', namespace='community')),
    path('admin/', include('adminapp.urls', namespace='admin')),
]

handler404 = mainapp.views.handler404

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [re_path(r'^__debug__/', include(debug_toolbar.urls))]
