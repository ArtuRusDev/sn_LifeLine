from django.urls import path
from profileapp.views import UserUpdateInfo, UserProfile, profile_base_view

app_name = 'profileapp'

urlpatterns = [
    path('', profile_base_view, name='info'),
    path('user/<pk>', UserProfile.as_view(), name='detail'),
    path('edit/', UserUpdateInfo.as_view(), name='edit'),
]
