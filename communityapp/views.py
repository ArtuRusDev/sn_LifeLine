from django.urls import reverse_lazy
from communityapp.forms import CreateCommunityForm, CreateCommunityNewsForm
from django.views.generic import CreateView, ListView, DetailView
from communityapp.models import Community, CommunityNewsItem


class CreateCommunityView(CreateView):
    model = Community
    template_name = 'communityapp/community_add.html'
    form_class = CreateCommunityForm
    success_url = reverse_lazy('news:main')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        self.object = form.save()
        return super().form_valid(form)


class CommunitiesListView(ListView):
    model = Community
    template_name = 'communityapp/community_list.html'


class CommunityDetailView(DetailView):
    model = Community
    template_name = 'communityapp/community_detail.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super(CommunityDetailView, self).get_context_data()
        data['news'] = CommunityNewsItem.objects.filter(community_id=self.kwargs['pk'])
        return data


class CreateCommunityNews(CreateView):
    model = CommunityNewsItem
    form_class = CreateCommunityNewsForm
    template_name = 'communityapp/community_create_news.html'
    success_url = reverse_lazy('community:main')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.community = Community.objects.get(pk=self.kwargs['pk'])
        form.save()
        return super().form_valid(form)
