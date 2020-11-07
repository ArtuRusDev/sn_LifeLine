from django.urls import path
from profileapp.views import ProfileView, UserUpdateInfo, UserProfile

app_name = 'profileapp'

urlpatterns = [
    path('', ProfileView.as_view(), name='info'),
    path('user/<pk>', UserProfile.as_view(), name='detail'),
    path('edit/', UserUpdateInfo.as_view(), name='edit'),
]
