from django.urls import path
import friendsapp.views as friendsapp

app_name = 'friendsapp'

urlpatterns = [
    path('', friendsapp.FriendsList.as_view(), name='main'),
    path('add/<pk>', friendsapp.send_friend_request, name='add'),
]
