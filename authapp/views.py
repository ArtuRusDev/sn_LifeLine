from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetConfirmView
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.generic import TemplateView, UpdateView

from authapp.forms import RegisterForm, LoginForm, ResetPasswordForm, UpdatePasswordForm
from authapp.models import Person
from mainapp.email import send_mail_async


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
                send_mail_async(
                    'Регистрация в социальной сети Life on Line',
                    f'{form.cleaned_data["first_name"]}, '
                    f'Добро пожаловать в социальную сеть Life on Line! Вы получили это письмо, так как прошли регистрацию на сайте life-online.ru.',
                    [str(form.cleaned_data["email"])])
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


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = ResetPasswordForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = Person.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Запрос на смену пароля"
                    email_template_name = "authapp/password/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    send_mail_async(subject, email, [user.email])

                    return redirect("auth:password_reset_done")
    password_reset_form = ResetPasswordForm()
    return render(request=request, template_name="authapp/password/password_reset.html",
                  context={"password_reset_form": password_reset_form})


class PassResetConfirmView(PasswordResetConfirmView):
    success_url = reverse_lazy('authapp:password_reset_complete')
    form_class = UpdatePasswordForm
