from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView

from authapp.models import Person


class ProfileView(TemplateView):
    template_name = "profileapp/profile.html"


class UserUpdateInfo(UpdateView):
    template_name = "authapp/login.html"
    model = Person
    success_url = reverse_lazy('main')
    # form_class = LoginForm