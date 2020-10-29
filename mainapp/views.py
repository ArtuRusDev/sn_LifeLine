from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, UpdateView

from authapp.models import Person


class NewsView(TemplateView):
    template_name = 'mainapp/news.html'


def main_page(request):
    # request.user.is_authenticated
    return HttpResponseRedirect(reverse('news'))
