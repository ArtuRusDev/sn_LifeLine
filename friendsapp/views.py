from django.db.models import Q
from django.http import HttpResponseBadRequest, JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from authapp.models import Person
from friendsapp.models import FriendRequests


class FriendsList(ListView):
    model = Person
    template_name = 'friendsapp/friends.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        data = {}
        user = self.request.user

        friend_requests = user.get_friend_requests
        friends = user.get_friends

        friends_pk = [friend.pk for friend in friends]
        friends_requests_pk = [friend.pk for friend in friend_requests]

        data['users'] = Person.objects.exclude(pk=user.pk)
        data['requests_pk'] = friends_requests_pk
        data['sent_requests_pk'] = user.get_send_friend_requests_pk
        data['friends_pk'] = friends_pk

        return data


@csrf_exempt
def update_friend_status(request, pk):
    if not request.is_ajax():
        return HttpResponseBadRequest('Invalid request')

    if request.method != 'POST' or request.POST.get('action') not in ('remove', 'accept', 'deny', 'add', 'cancel'):
        return JsonResponse({'status': 'Invalid request'}, status=400)

    if request.POST.get('action') == 'remove':
        try:
            friend_request = FriendRequests.objects.get(initiator=Person.objects.get(pk=pk), target=request.user)
        except Exception:
            friend_request = FriendRequests.objects.get(initiator=request.user, target=Person.objects.get(pk=pk))
            friend_request.initiator = Person.objects.get(pk=pk)
            friend_request.target = request.user

        friend_request.status = 0
        friend_request.save()

        result = {
            'status': 'Friend removed',
            'content': render_to_string('friendsapp/includes/inc_friend_item.html',
                                        {'usr': Person.objects.get(pk=pk), 'requests_pk': [int(pk)]})
        }
    elif request.POST.get('action') == 'cancel':
        friend_request = FriendRequests.objects.get(initiator=request.user, target=Person.objects.get(pk=pk))
        friend_request.status = 3
        friend_request.save()

        result = {
            'status': 'Request canceled',
            'content': render_to_string('friendsapp/includes/inc_friend_item.html',
                                        {'usr': Person.objects.get(pk=pk)})
        }

    elif request.POST.get('action') == 'add':
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

        result = {
            'status': 'Friend request sent',
            'content': render_to_string('friendsapp/includes/inc_friend_item.html',
                                        {'usr': Person.objects.get(pk=pk), 'sent_requests_pk': [int(pk)]})
        }
    elif request.POST.get('action') == 'accept':
        try:
            friend_request = FriendRequests.objects.get(initiator=Person.objects.get(pk=pk), target=request.user)
        except Exception:
            friend_request = FriendRequests.objects.get(initiator=request.user, target=Person.objects.get(pk=pk))

        friend_request.status = 1
        friend_request.save()

        result = {
            'status': 'Request accepted',
            'content': render_to_string('friendsapp/includes/inc_friend_item.html',
                                        {'usr': Person.objects.get(pk=pk), 'friends_pk': [int(pk)]})
        }
    else:
        try:
            friend_request = FriendRequests.objects.get(initiator=Person.objects.get(pk=pk), target=request.user)
        except Exception:
            friend_request = FriendRequests.objects.get(initiator=request.user, target=Person.objects.get(pk=pk))

        friend_request.status = 3
        friend_request.save()

        result = {
            'status': 'Request denied',
            'content': render_to_string('friendsapp/includes/inc_friend_item.html',
                                        {'usr': Person.objects.get(pk=pk), 'requests_pk': [int(pk)]})
        }

    return JsonResponse(result)