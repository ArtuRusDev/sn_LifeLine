from django.http import HttpResponseRedirect
from django.shortcuts import render

from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView

from newsapp.forms import CreateNewsForm
from newsapp.models import NewsItem


class NewsView(ListView):
    model = NewsItem
    template_name = 'newsapp/news.html'

    def get_queryset(self):
        queryset = NewsItem.objects.all().order_by('-add_datetime')
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

# def delete_news(request, news_id):
#     news_item = NewsItem.objects.get(pk=news_id)
#     if request.user == news_item.user:
#         news_item.delete()
#
#     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
