from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, UpdateView, DetailView
from authapp.models import Person
from newsapp.models import NewsItem
from profileapp.forms import UserUpdateInfoForm


def profile_base_view(request):
    return redirect(reverse('profile:detail', kwargs={'pk': request.user.pk}))


class UserUpdateInfo(UpdateView):
    template_name = "profileapp/profile_edit.html"
    model = Person
    form_class = UserUpdateInfoForm
    success_url = reverse_lazy('profile:edit')

    def get_object(self, *args, **kwargs):
        return get_object_or_404(Person, pk=self.request.user.pk)


class UserProfile(DetailView):
    template_name = "profileapp/profile.html"
    model = Person

    def get_context_data(self, **kwargs):
        data = super(UserProfile, self).get_context_data(**kwargs)

        user = get_object_or_404(Person, pk=self.kwargs['pk'])
        news = NewsItem.objects.filter(user__pk=user.pk).order_by('-add_datetime')

        is_friend = user.pk in self.request.user.get_friends_pk
        data['cur_user'] = user
        data['news'] = news
        data['is_friend'] = is_friend

        return data
