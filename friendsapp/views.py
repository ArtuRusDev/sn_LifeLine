from django.http import HttpResponseRedirect
from django.views.generic import ListView
from authapp.models import Person
from friendsapp.models import FriendRequests


def send_friend_request(request, pk):
    # Получаю все дупликаты запроса на добавление в друзья
    try:
        duplicate = FriendRequests.objects.filter(initiator=Person.objects.get(pk=pk), target=request.user)
    except Exception:
        try:
            duplicate = FriendRequests.objects.filter(initiator=request.user, target=Person.objects.get(pk=pk))
        except Exception:
            duplicate = []

    if not duplicate:
        friend_request = FriendRequests.objects.create(initiator=request.user, target=Person.objects.get(pk=pk))
        friend_request.save()
    else:
        friend_request = duplicate[0]
        # Изменение статуса на "запрошено" только если статус уже не стоит как "подтвержденный"
        if friend_request.status != 1:
            friend_request.status = 0
            friend_request.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class FriendsList(ListView):
    model = FriendRequests
    template_name = 'friendsapp/friends.html'
