from django.shortcuts import render, redirect
from django.urls import reverse

from messengerapp.forms import MessageForm
from messengerapp.models import Chat
from django.views import View
from django.views.generic import TemplateView


class DialogsView(TemplateView):
    template_name = 'messengerapp/dialogs.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super(DialogsView, self).get_context_data()
        data['chats'] = Chat.objects.filter(members__in=[self.request.user.id])
        # data['chats'] = Chat.objects.all()
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
                'form': MessageForm()
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
