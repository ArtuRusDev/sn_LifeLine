from django.urls import path

import communityapp.views as communityapp

app_name = 'communityapp'

urlpatterns = [
    path('', communityapp.CommunitiesListView.as_view(), name='main'),
    path('<pk>/', communityapp.CommunityDetailView.as_view(), name='create'),
    path('create/', communityapp.CreateCommunityView.as_view(), name='create'),
]
