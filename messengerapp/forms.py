from django.forms import ModelForm

from messengerapp.models import Message


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['message']
        labels = {'message': ""}
