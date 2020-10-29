from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView
from authapp.models import Person
from profileapp.forms import UserUpdateInfoForm


class ProfileView(TemplateView):
    template_name = "profileapp/profile.html"


class UserUpdateInfo(UpdateView):
    template_name = "profileapp/profile_edit.html"
    model = Person
    form_class = UserUpdateInfoForm
    success_url = reverse_lazy('profile:edit')

    def get_object(self, *args, **kwargs):
        return get_object_or_404(Person, pk=self.request.user.pk)
