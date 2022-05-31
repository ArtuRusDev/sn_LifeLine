from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic import ListView, UpdateView, DeleteView, CreateView, TemplateView

from adminapp.forms import UserUpdateForm, UpdateNewsForm
from authapp.models import Person
from communityapp.models import Community
from friendsapp.models import FriendRequests
from messengerapp.models import Chat, Message
from newsapp.forms import CreateNewsForm
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


class DeleteUserView(DeleteView):
    model = Person
    template_name = 'adminapp/user_confirm_delete.html'
    success_url = reverse_lazy('admin:user_read')


class NewsList(ListView):
    model = NewsItem
    template_name = 'adminapp/news.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        data = {'news': NewsItem.objects.all()}
        return data


class CreateNewsItem(CreateView):
    model = NewsItem
    form_class = CreateNewsForm
    template_name = 'newsapp/create_news.html'
    success_url = reverse_lazy('admin:news_read')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.add_datetime = timezone.now()
        self.object = form.save()
        return super().form_valid(form)


class ModerateNewsList(ListView):
    model = NewsItem
    template_name = 'adminapp/news_moderate.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        data = {'news': NewsItem.objects.filter(is_moderated=0)}
        return data


class NewsUpdate(UpdateView):
    model = NewsItem
    form_class = UpdateNewsForm
    template_name = 'adminapp/update_news.html'
    success_url = reverse_lazy('admin:news_read')

    def form_valid(self, form):
        form.instance.is_moderated = 0
        form.instance.is_accepted = 0
        form.instance.add_datetime = timezone.now()
        self.object = form.save()
        return super().form_valid(form)


class DeleteNewsView(DeleteView):
    model = NewsItem
    template_name = 'newsapp/confirm_delete.html'
    success_url = reverse_lazy('admin:news_read')


class StatisticView(TemplateView):
    template_name = 'adminapp/statistic.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        data = {
            'users': Person.objects.all(),
            'communities': Community.objects.all(),
            'news': NewsItem.objects.all(),
            'dialogs': Chat.objects.filter(type="D"),
            'chats': Chat.objects.filter(type="C"),
            'messages': Message.objects.all(),
            'community_news': NewsItem.objects.filter(is_community=True),
            'friend_request': FriendRequests.objects.all(),
            'accepted_request': FriendRequests.objects.filter(status=1),
        }


        return data


def accept_news(request, pk):
    if request.is_ajax():
        NewsItem.objects.filter(pk=pk).update(is_accepted=1, is_moderated=True)

        return JsonResponse({'result': 'success'})


def cancel_news(request, pk):
    if request.is_ajax():
        NewsItem.objects.filter(pk=pk).update(is_accepted=0, is_moderated=True)

        return JsonResponse({'result': 'success'})
