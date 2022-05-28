from itertools import chain

from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from django.http import JsonResponse, Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView
from django.template.loader import render_to_string

from communityapp.models import CommunityNewsItem, CommunityParticipant, Community

from newsapp.forms import CreateNewsForm
from newsapp.models import NewsItem, Likes, Comments


class NewsView(ListView):
    model = NewsItem
    template_name = 'newsapp/news.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        data = {}
        user = self.request.user
        friends = user.get_friends
        friends_pk = [friend.pk for friend in friends]
        friend_requests_users_pk = user.get_send_friend_requests_pk

        all_subscribed_communities = CommunityParticipant.objects.filter(user_id=self.request.user)
        all_own_communities = Community.objects.filter(creator_id=self.request.user)

        all_com_ids = [instance.community_id for instance in all_subscribed_communities]
        all_com_ids += [community.id for community in all_own_communities]

        all_community_news = CommunityNewsItem.objects.filter(community_id__in=all_com_ids).select_related()
        all_community_news_id = [community.id for community in all_community_news]

        all_news = NewsItem.objects.filter((
                Q(user__pk__in=friends_pk) | Q(user__pk__in=friend_requests_users_pk) | Q(user__pk=user.pk) &
                ((~Q(is_accepted=0) & Q(is_moderated=1)) | Q(is_moderated=0)) &
                Q(is_community=False))).exclude(pk__in=all_community_news_id).filter(
            is_community=False).select_related()

        data['all_news'] = sorted(chain(all_news, all_community_news),
                                  key=lambda instance: instance.add_datetime, reverse=True)
        data['all_comments'] = Comments.objects.all()

        return data


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

    def get_context_data(self, **kwargs):
        data = super(DeleteNewsView, self).get_context_data()

        news_owner_pk = NewsItem.objects.get(pk=self.kwargs['pk']).user.pk
        user_pk = self.request.user.pk

        if user_pk != news_owner_pk:
            raise Http404("You can't delete someone else's record")
        return data


def add_comment(request):
    if request.method == 'POST':
        news_pk = request.POST.get('news_pk')
        content = request.POST.get('content')

        if content:
            Comments.objects.create(news_item=NewsItem.objects.get(id=news_pk), author=request.user, text=content)
        else:
            return JsonResponse({'result': 'empty_input'})

        context = {
            'news_item': NewsItem.objects.get(pk=news_pk),
            'user': request.user
        }

        result = {
            'comments_html': render_to_string('newsapp/includes/comments_list_block.html', context),
            'comments_cnt': Comments.objects.filter(news_item_id=news_pk).count(),
        }

        return JsonResponse(result)


def add_news(request):
    if request.method == 'POST':
        text = request.POST.get('text')

        if request.FILES:
            file = request.FILES['image']
            NewsItem.objects.create(user=request.user, text=text, image=file)
        else:
            NewsItem.objects.create(user=request.user, text=text)

    return redirect('/')


def delete_comment(request, pk):
    comment_item = Comments.objects.get(pk=pk)
    comment_news = comment_item.news_item
    comment_item.delete()
    total_comments_cnt = Comments.objects.filter(news_item_id=comment_news.id).count()

    result = {
        'comments_cnt': total_comments_cnt,
        'comments_html': render_to_string('newsapp/includes/comments_list_block.html',
                                          {'news_item': NewsItem.objects.get(pk=comment_news.id),
                                           'user': request.user}),
        'news_id': comment_news.id
    }

    return JsonResponse(result)


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
