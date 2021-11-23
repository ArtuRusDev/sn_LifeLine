from django.urls import path
import newsapp.views as newsapp

app_name = 'newsapp'

urlpatterns = [
    path('', newsapp.NewsView.as_view(), name='main'),
    path('create/', newsapp.CreateNews.as_view(), name='create'),
    path('delete/<pk>/', newsapp.DeleteNewsView.as_view(), name='delete'),
    path('like/<pk>/', newsapp.put_like, name='put_like'),
    path('add_comment/', newsapp.add_comment, name="add_comment"),
    path('delete_comment/<pk>/', newsapp.delete_comment, name="delete_comment")
]
