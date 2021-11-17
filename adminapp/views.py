from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, UpdateView, DeleteView

from adminapp.forms import UserUpdateForm, UpdateNewsForm
from authapp.models import Person
from newsapp.models import NewsItem


def main_page(request):
    return HttpResponseRedirect(reverse('admin:user_read'))


class UsersList(ListView):
    model = Person
    template_name = 'adminapp/users.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        data = {'users': Person.objects.all()}
        return data


class UserUpdate(UpdateView):
    model = Person
    form_class = UserUpdateForm
    template_name = 'adminapp/update_user.html'
    success_url = reverse_lazy('admin:user_read')


class NewsList(ListView):
    model = NewsItem
    template_name = 'adminapp/news.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        data = {'news': NewsItem.objects.all()}
        return data


class NewsUpdate(UpdateView):
    model = NewsItem
    form_class = UpdateNewsForm
    template_name = 'adminapp/update_news.html'
    success_url = reverse_lazy('admin:news_read')


class DeleteNewsView(DeleteView):
    model = NewsItem
    template_name = 'newsapp/confirm_delete.html'
    success_url = reverse_lazy('admin:news_read')
