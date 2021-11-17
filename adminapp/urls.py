from django.urls import path
import adminapp.views as adminapp

app_name = 'adminapp'

urlpatterns = [
    path('', adminapp.main_page, name='main'),
    path('users/read/', adminapp.UsersList.as_view(), name='user_read'),
    path('users/update/<pk>/', adminapp.UserUpdate.as_view(), name='user_update'),

    path('news/read/', adminapp.NewsList.as_view(), name='news_read'),
    path('news/update/<pk>/', adminapp.NewsUpdate.as_view(), name='news_update'),
    path('news/delete/<pk>/', adminapp.DeleteNewsView.as_view(), name='news_delete'),
]
