from django.urls import path

import communityapp.views as communityapp

app_name = 'communityapp'

urlpatterns = [
    path('', communityapp.CommunitiesListView.as_view(), name='main'),
    path('create/', communityapp.CreateCommunityView.as_view(), name='create'),
    path('<pk>/add_news/', communityapp.CreateCommunityNews.as_view(), name='add_news'),
    path('<pk>/', communityapp.CommunityDetailView.as_view(), name='detail'),
]
