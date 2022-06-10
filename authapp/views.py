from django.contrib.auth import logout, login, authenticate
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView, UpdateView

from authapp.forms import RegisterForm, LoginForm
from authapp.models import Person


class UserRegisterView(TemplateView):
    template_name = "authapp/register.html"

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = RegisterForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                new_user = authenticate(username=form.cleaned_data['username'], 
                    password=form.cleaned_data['password1'])
                login(request, new_user)
                return HttpResponseRedirect(reverse('news:main'))
        else:
            form = RegisterForm()

        content = {
            'title': 'Регистрация',
            'form': form
        }

        return render(request, self.template_name, content)


class UserLoginView(LoginView):
    template_name = "authapp/login.html"
    model = Person
    success_url = reverse_lazy('main')
    form_class = LoginForm


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('main')
