from django.db.models import Q
from django.http import HttpResponseRedirect
from django.views.generic import ListView
from authapp.models import Person
from friendsapp.models import FriendRequests


def send_friend_request(request, pk):
    # Получаю запрос в друзья между пользователями если такой есть
    duplicate = FriendRequests.objects.filter(Q(initiator=Person.objects.get(pk=pk), target=request.user) |
                                              Q(initiator=request.user, target=Person.objects.get(pk=pk)))

    if not duplicate:
        friend_request = FriendRequests.objects.create(initiator=request.user, target=Person.objects.get(pk=pk))
        friend_request.save()
    else:
        friend_request = duplicate[0]
        # Изменение статуса на "запрошено" только если статус уже не стоит как "подтвержденный"
        if friend_request.status != 1:
            friend_request.delete()

            friend_request = FriendRequests.objects.create(initiator=request.user, target=Person.objects.get(pk=pk))
            friend_request.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def remove_from_friends(request, pk):
    try:
        friend_request = FriendRequests.objects.get(initiator=Person.objects.get(pk=pk), target=request.user)
    except Exception:
        friend_request = FriendRequests.objects.get(initiator=request.user, target=Person.objects.get(pk=pk))

    friend_request.status = 2
    friend_request.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def confirm_friend_request(request, pk):
    try:
        friend_request = FriendRequests.objects.get(initiator=Person.objects.get(pk=pk), target=request.user)
    except Exception:
        friend_request = FriendRequests.objects.get(initiator=request.user, target=Person.objects.get(pk=pk))

    friend_request.status = 1
    friend_request.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def deny_friend_request(request, pk):
    try:
        friend_request = FriendRequests.objects.get(initiator=Person.objects.get(pk=pk), target=request.user)
    except Exception:
        friend_request = FriendRequests.objects.get(initiator=request.user, target=Person.objects.get(pk=pk))

    friend_request.status = 3
    friend_request.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class FriendsList(ListView):
    model = FriendRequests
    template_name = 'friendsapp/friends.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super(FriendsList, self).get_context_data()

        friends_pk = [friend.pk for friend in self.request.user.get_friends]

        friends_requests_pk = [friend.pk for friend in self.request.user.get_friend_requests]

        data['all_users'] = Person.objects.exclude(pk=self.request.user.pk).exclude(pk__in=friends_pk).exclude(pk__in=friends_requests_pk)
        data['send_requests_pk'] = self.request.user.get_send_friend_requests_pk

        return data
