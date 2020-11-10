from django.http import HttpResponseRedirect
from django.views.generic import ListView
from authapp.models import Person
from friendsapp.models import FriendRequests


def send_friend_request(request, pk):
    friend_request = FriendRequests.objects.create(initiator=request.user, target=Person.objects.get(pk=pk))
    friend_request.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class FriendsList(ListView):
    model = FriendRequests
    # template_name =