from django.urls import path
import friendsapp.views as friendsapp

app_name = 'friendsapp'

urlpatterns = [
    path('add/<pk>', friendsapp.send_friend_request, name='add'),
]
