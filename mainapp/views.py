from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.views.generic import TemplateView


class NewsView(TemplateView):
    template_name = 'mainapp/news.html'


def main_page(request):
    return HttpResponseRedirect(reverse('news'))
