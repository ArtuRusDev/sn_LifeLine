from itertools import chain

from django.http import JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy

from authapp.models import Person
from communityapp.forms import CreateCommunityForm, CreateCommunityNewsForm
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from communityapp.models import Community, CommunityNewsItem, CommunityParticipant


class CreateCommunityView(CreateView):
    model = Community
    template_name = 'communityapp/add.html'
    form_class = CreateCommunityForm
    success_url = reverse_lazy('community:main')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        self.object = form.save()
        return super().form_valid(form)


class CommunitiesListView(ListView):
    model = Community
    template_name = 'communityapp/list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super(CommunitiesListView, self).get_context_data()

        all_subscribed_communities = CommunityParticipant.objects.filter(user_id=self.request.user)
        all_ids = [instance.community_id for instance in all_subscribed_communities]

        subscribed_communities = Community.objects.filter(pk__in=all_ids)
        unsubscribed_communities = Community.objects.exclude(pk__in=all_ids)

        data['communities'] = chain(subscribed_communities, unsubscribed_communities)
        data['subscribed_communities_id'] = all_ids
        return data


class CommunityUpdateView(UpdateView):
    model = Community
    form_class = CreateCommunityForm
    template_name = 'communityapp/update.html'
    success_url = reverse_lazy('community:main')


class CommunityDeleteView(DeleteView):
    model = Community
    template_name = 'communityapp/confirm_delete.html'
    success_url = reverse_lazy('community:main')


class CommunityDetailView(DetailView):
    model = Community
    template_name = 'communityapp/detail.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super(CommunityDetailView, self).get_context_data()
        data['news'] = CommunityNewsItem.objects.filter(community_id=self.kwargs['pk'])
        data['is_publisher'] = self.request.user.id in kwargs['object'].get_publishers_id or \
                               kwargs['object'].creator.id == self.request.user.id
        return data


class CommunityModeratorsView(DetailView):
    model = Community
    template_name = 'communityapp/moderators.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super(CommunityModeratorsView, self).get_context_data()
        data['publishers_id'] = kwargs['object'].get_publishers_id
        data['subscribers_id'] = kwargs['object'].get_subscribers_id
        data['users'] = Person.objects.filter(id__in=data['subscribers_id']).exclude(id=self.request.user.id)
        return data


class CreateCommunityNews(CreateView):
    model = CommunityNewsItem
    form_class = CreateCommunityNewsForm
    template_name = 'communityapp/create_news.html'
    success_url = reverse_lazy('community:main')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.community = Community.objects.get(pk=self.kwargs['pk'])
        form.instance.is_community = True
        form.save()
        return super().form_valid(form)


def subscribe_community(request, pk):
    if request.is_ajax():
        duplicate = CommunityParticipant.objects.filter(user=request.user, community_id=pk)
        subscribed_communities = []

        if not duplicate:
            record = CommunityParticipant.objects.create(user=request.user, community_id=pk)
            record.save()
            subscribed_communities.append(int(pk))
        else:
            duplicate[0].delete()

        context = {
            'community': Community.objects.get(pk=pk),
            'subscribed_communities_id': subscribed_communities,
            'user': request.user
        }

        print(context)

        result = {
            'result': render_to_string('communityapp/includes/community-card-item.html', context)
        }

        return JsonResponse(result)


def change_publisher(request):
    if request.is_ajax():
        context = {}
        instance = CommunityParticipant.objects.get(
            user_id=request.POST.get('user'),
            community_id=request.POST.get('community')
        )
        if instance.role == 0:
            instance.role = 1
            context.update({'is_publisher': True})
        else:
            instance.role = 0
            context.update({'is_publisher': False})
        instance.save()
        print(context)

        return JsonResponse(context)
