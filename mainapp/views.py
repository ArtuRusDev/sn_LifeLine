from django.http import HttpResponseRedirect
from django.urls import reverse


def main_page(request):
    return HttpResponseRedirect(reverse('news:main'))
