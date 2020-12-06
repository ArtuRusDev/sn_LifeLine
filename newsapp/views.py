from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView
from newsapp.forms import CreateNewsForm
from newsapp.models import NewsItem, Likes
from django.template.loader import render_to_string


class NewsView(ListView):
    model = NewsItem
    template_name = 'newsapp/news.html'

    def get_queryset(self):
        friends_pk = self.request.user.get_friends_pk
        friend_requests_users_pk = self.request.user.get_send_friend_requests_pk
        queryset = NewsItem.objects.filter(Q(user__pk__in=friends_pk) | Q(user__pk__in=friend_requests_users_pk) |
                                           Q(user__pk=self.request.user.pk)).order_by('-add_datetime').select_related()
        return queryset


class CreateNews(CreateView):
    model = NewsItem
    form_class = CreateNewsForm
    template_name = 'newsapp/create_news.html'
    success_url = reverse_lazy('news:main')

    def form_valid(self, form):
        form.instance.user = self.request.user
        self.object = form.save()
        return super().form_valid(form)


class DeleteNewsView(DeleteView):
    model = NewsItem
    template_name = 'newsapp/confirm_delete.html'
    success_url = reverse_lazy('profile:info')


def put_like(request, pk):
    if request.is_ajax():
        duplicate = Likes.objects.filter(user=request.user, news_item_id=pk)

        if not duplicate:
            record = Likes.objects.create(user=request.user, news_item_id=pk)
            record.save()
        else:
            Likes.objects.filter(user=request.user, news_item_id=pk).delete()

        context = {
            'user': request.user,
            'news_item': NewsItem.objects.get(pk=pk)
        }

        result = render_to_string('newsapp/includes/likes_block.html', context)

        return JsonResponse({'result': result})
