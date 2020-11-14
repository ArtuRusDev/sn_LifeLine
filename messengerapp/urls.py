from django.conf.urls import url
from django.urls import path
import messengerapp.views as messengerapp

app_name = 'messenger'

urlpatterns = [
    path('', messengerapp.DialogsView.as_view(), name='dialogs'),
    path('<chat_id>/', messengerapp.MessagesView.as_view(), name='messages'),
    path('get_messages/<chat_id>/', messengerapp.get_messages, name='get_messages'),
    # url(r'^dialogs/create/(?P<user_id>\d+)/$', messengerapp.CreateDialogView.as_view(), name='create_dialog'),
]
