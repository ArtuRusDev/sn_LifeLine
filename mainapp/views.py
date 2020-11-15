from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


def main_page(request):
    return HttpResponseRedirect(reverse('news:main'))


def handler404(request, exception):
    return render(request, 'mainapp/404.html', {})
