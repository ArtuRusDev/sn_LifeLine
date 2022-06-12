from django.urls import path
import friendsapp.views as friendsapp

app_name = 'friendsapp'

urlpatterns = [
    path('', friendsapp.FriendsList.as_view(), name='main'),
    path('update_status/<pk>', friendsapp.update_friend_status, name='update')
]
