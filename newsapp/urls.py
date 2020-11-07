from django.urls import path
import newsapp.views as newsapp

app_name = 'newsapp'

urlpatterns = [
    path('', newsapp.NewsView.as_view(), name='main'),
    path('create/', newsapp.CreateNews.as_view(), name='create'),
]
