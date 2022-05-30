from django.db.models import Q
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from authapp.models import Person
from messengerapp.forms import MessageForm, CreateChatForm
from messengerapp.models import Chat
from django.views import View
from django.views.generic import TemplateView, CreateView, UpdateView


class DialogsView(TemplateView):
    template_name = 'messengerapp/dialogs.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super(DialogsView, self).get_context_data()
        data['chats'] = Chat.objects.filter(members__in=[self.request.user.id])

        return data


class MessagesView(View):
    def get(self, request, chat_id):
        try:
            chat = Chat.objects.get(id=chat_id)
            if request.user in chat.members.all():
                chat.message_set.filter(is_read=False).exclude(author=request.user).update(is_read=True)
            else:
                chat = None
        except Chat.DoesNotExist:
            chat = None

        return render(
            request,
            'messengerapp/messages.html',
            {
                'chat': chat,
                'form': MessageForm(),
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
    duplicate = Chat.objects.filter(members__id__contains=friend_id, type='D') & \
                Chat.objects.filter(members__id__icontains=request.user.pk, type='D')
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


def get_messages(request, chat_id):
    if request.is_ajax():
        try:
            chat = Chat.objects.get(id=chat_id)

            if not chat.last_message:
                return JsonResponse({'result': False})

            # Проверка, что сообщение не прочитано и автор не текущий пользователь
            is_update = chat.last_message.author != request.user and not chat.last_message.is_read

            if is_update:
                if request.user in chat.members.all():
                    chat.message_set.filter(is_read=False).exclude(author=request.user).update(is_read=True)
                else:
                    chat = None
            else:
                return JsonResponse({'result': False})
        except Chat.DoesNotExist:
            chat = None

        context = {
            'chat': chat,
            'user': request.user,
        }

        result = render_to_string('messengerapp/includes/message_dialog.html', context)

        return JsonResponse({'result': result})


def get_new_mes_count(request):
    user = request.user
    new_mess_count = user.chat_set.unreaded(user=user).count()
    if new_mess_count == 0:
        return JsonResponse({'result': False})

    return JsonResponse({'result': new_mess_count})


def update_chats_list(request):
    if request.is_ajax():
        context = {
            'user': request.user,
            'chats': Chat.objects.filter(members__in=[request.user.id]),
            'unread_chats': request.user.chat_set.unreaded(user=request.user)
        }

        result = render_to_string('messengerapp/includes/chats_list.html', context)

        return JsonResponse({'result': result})
