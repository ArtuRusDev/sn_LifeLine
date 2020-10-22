from django.contrib import messages, auth
from django.contrib.auth import logout, login
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView

from authapp.forms import RegisterForm, LoginForm


class RegisterView(TemplateView):
    template_name = "authapp/register.html"

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = RegisterForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, "Вы успешно зарегистрировались!")
                return HttpResponseRedirect(reverse('auth:login'))
        else:
            form = RegisterForm()

        content = {
            'title': 'Регистрация',
            'form': form
        }

        return render(request, self.template_name, content)


class LoginView(View):
    template_name = "authapp/login.html"

    def dispatch(self, request, *args, **kwargs):
        form = LoginForm(request.POST)

        if request.method == 'POST' and form.is_valid:
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                messages.success(request, "Вы успешно вошли!")
                return HttpResponseRedirect(reverse('main'))
        else:
            form = LoginForm()

        content = {
            'title': 'Вход',
            'form': form
        }

        return render(request, self.template_name, content)


class LogoutView(View):
    def dispatch(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, "Вы успешно вышли!")
        return HttpResponseRedirect(reverse('main'))


class ProfileView(TemplateView):
    template_name = "authapp/profile.html"
