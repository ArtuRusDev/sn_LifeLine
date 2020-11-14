from django.conf.urls import url
from django.urls import path
import messengerapp.views as messengerapp

app_name = 'messenger'

urlpatterns = [
    path('', messengerapp.DialogsView.as_view(), name='dialogs'),
    path('<chat_id>/', messengerapp.MessagesView.as_view(), name='messages'),
    path('get_messages/<chat_id>/', messengerapp.get_messages, name='get_messages'),
    path('create/<friend_id>/', messengerapp.create_dialog, name='create_dialog'),
    path('delete/<chat_id>/', messengerapp.delete_dialog, name='delete_chat'),
]
