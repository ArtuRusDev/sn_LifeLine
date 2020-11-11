from django.urls import path
import friendsapp.views as friendsapp

app_name = 'friendsapp'

urlpatterns = [
    path('', friendsapp.FriendsList.as_view(), name='main'),
    path('add/<pk>', friendsapp.send_friend_request, name='add'),
    path('remove/<pk>', friendsapp.remove_from_friends, name='remove'),
    path('confirm/<pk>', friendsapp.confirm_friend_request, name='confirm'),
    path('deny/<pk>', friendsapp.deny_friend_request, name='deny'),
]
