import operator
from functools import reduce

from django.db.models import Q
from django.http import JsonResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, CreateView, UpdateView

from authapp.models import Person
from messengerapp.forms import MessageForm, CreateChatForm
from messengerapp.models import Chat, Message


class DialogsView(TemplateView):
    template_name = 'messengerapp/dialogs.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super(DialogsView, self).get_context_data()
        data['chats'] = Chat.objects.filter(members__in=[self.request.user.id])
        data['unread_msg_cnt'] = {}

        for chat in data['chats']:
            unread_cnt = len(Message.objects.filter(chat__pk=chat.pk, is_read=False))
            if unread_cnt > 99:
                unread_cnt = '99+'
            data['unread_msg_cnt'].update({chat.pk: unread_cnt})

        return data


class MessagesView(View):
    def get(self, request, chat_id):
        try:
            chat = Chat.objects.get(id=chat_id)
            if request.user not in chat.members.all():
                return redirect('messenger:dialogs')

            chat.message_set.filter(is_read=False).exclude(author=request.user).update(is_read=True)

        except Chat.DoesNotExist:
            return redirect('messenger:dialogs')

        messages_list = chat.message_set.all()

        dates = {}
        prev_msg_date = ''

        for msg in messages_list:
            if not prev_msg_date or msg.pub_date.strftime('%d.%m.%Y') != prev_msg_date:
                dates.update({msg.pk: msg.pub_date.strftime('%d %B %Y')})
            prev_msg_date = msg.pub_date.strftime('%d.%m.%Y')

        return render(
            request,
            'messengerapp/messages.html',
            {
                'chat': chat,
                'form': MessageForm(),
                'messages_list': messages_list,
                'dates': dates
            }
        )

    def post(self, request, chat_id):
        form = MessageForm(data=request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.chat_id = chat_id
            message.author = request.user
            message.save()
        return redirect(reverse('messenger:messages', kwargs={'chat_id': chat_id}))


class CreateChatView(CreateView):
    model = Chat
    template_name = 'messengerapp/add_chat.html'
    form_class = CreateChatForm
    success_url = reverse_lazy('messenger:dialogs')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        self.object = form.save()
        return super().form_valid(form)


class EditChatView(UpdateView):
    model = Chat
    template_name = 'messengerapp/edit_chat.html'
    form_class = CreateChatForm
    success_url = reverse_lazy('messenger:dialogs')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        self.object = form.save()
        return super().form_valid(form)


def create_dialog(request, friend_id):
    duplicate = Chat.objects.filter(members__id__in=[friend_id], type='D').filter(members__in=[request.user], type='D')

    if duplicate.exists():
        return redirect(reverse('messenger:messages', kwargs={'chat_id': duplicate[0].pk}))

    chat = Chat.objects.create(type='D')
    members = Person.objects.filter(pk__in=[friend_id, request.user.pk])
    chat.members.add(*members)
    return redirect(reverse('messenger:messages', kwargs={'chat_id': chat.pk}))


def delete_dialog(request, chat_id):
    chat = get_object_or_404(Chat, pk=chat_id)
    chat.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@csrf_exempt
def update_chats_list(request):
    if not request.is_ajax():
        return HttpResponseBadRequest('Invalid request')

    if request.method != 'POST':
        return JsonResponse({'status': 'Invalid request'}, status=400)

    context = {
        'user': request.user,
        'chats': Chat.objects.filter(members__in=[request.user.id]),
        'unread_chats': request.user.chat_set.unreaded(user=request.user),
        'unread_msg_cnt': {}
    }

    for chat in context['chats']:
        unread_cnt = len(Message.objects.filter(chat__pk=chat.pk, is_read=False))
        if unread_cnt > 99:
            unread_cnt = '99+'
        context['unread_msg_cnt'].update({chat.pk: unread_cnt})

    result = render_to_string('messengerapp/includes/chats_list.html', context)

    return JsonResponse({'result': result})
