from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse, HttpResponseNotFound, Http404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from newsapp.forms import CreateNewsForm
from newsapp.models import NewsItem, Likes
from django.template.loader import render_to_string
from django.utils import timezone


class NewsView(ListView):
    model = NewsItem
    template_name = 'newsapp/news.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        data = {}
        user = self.request.user
        friends = user.get_friends
        friends_pk = [friend.pk for friend in friends]
        friend_requests_users_pk = user.get_send_friend_requests_pk
        data['all_news'] = NewsItem.objects.filter((
                Q(user__pk__in=friends_pk) | Q(user__pk__in=friend_requests_users_pk) | Q(user__pk=user.pk) &
                ((~Q(is_accepted=0) & Q(is_moderated=1)) | Q(is_moderated=0)))
        ).select_related().order_by('-add_datetime')
        return data


class CreateNews(CreateView):
    model = NewsItem
    form_class = CreateNewsForm
    template_name = 'newsapp/create_news.html'
    success_url = reverse_lazy('news:main')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.add_datetime = timezone.now()
        self.object = form.save()
        return super().form_valid(form)


class DeleteNewsView(DeleteView):
    model = NewsItem
    template_name = 'newsapp/confirm_delete.html'
    success_url = reverse_lazy('profile:info')

    def get_context_data(self, **kwargs):
        data = super(DeleteNewsView, self).get_context_data()

        news_owner_pk = NewsItem.objects.get(pk=self.kwargs['pk']).user.pk
        user_pk = self.request.user.pk

        if user_pk != news_owner_pk:
            raise Http404("You can't delete someone else's record")
        return data


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
