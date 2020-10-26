from django.urls import path
import authapp.views as authapp

app_name = 'authapp'

urlpatterns = [
    path('login/', authapp.UsersLoginView.as_view(), name='login'),
    path('logout/', authapp.UsersLogoutView.as_view(), name='logout'),
    path('regitster/', authapp.RegisterView.as_view(), name='register'),
    path('profile/', authapp.ProfileView.as_view(), name='profile'),
]
