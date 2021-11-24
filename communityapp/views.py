from django.urls import reverse_lazy
from communityapp.forms import CreateCommunityForm
from django.views.generic import CreateView, ListView, DetailView
from communityapp.models import Community


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
