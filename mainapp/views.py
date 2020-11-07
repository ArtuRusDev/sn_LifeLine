from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, UpdateView

from authapp.models import Person


def main_page(request):
    return HttpResponseRedirect(reverse('news:main'))
