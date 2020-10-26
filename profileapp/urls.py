from django.urls import path
from profileapp.views import ProfileView, UserUpdateInfo

app_name = 'profileapp'

urlpatterns = [
    path('', ProfileView.as_view(), name='info'),
    path('edit/', UserUpdateInfo.as_view(), name='edit'),
]
