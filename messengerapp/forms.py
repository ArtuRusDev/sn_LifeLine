from itertools import chain

from django.db.models import QuerySet
from django.forms import ModelForm

from authapp.models import Person
from messengerapp.models import Message, Chat


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['message']
        labels = {'message': ""}


class CreateChatForm(ModelForm):
    class Meta:
        model = Chat
        fields = ("title", "members")

    def __init__(self, *args, **kwargs):
        super(CreateChatForm, self).__init__(*args, **kwargs)
        # print(data)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'b-form__input'
            field.widget.attrs["placeholder"] = self.Meta.model._meta.get_field(field_name).verbose_name.capitalize
            field.help_text = ""

            if field_name == 'members':
                field.label = 'Участники (Выберите с зажатым Ctrl)'

    def clean_members(self):
        user_qset = Person.objects.filter(pk=self.data['user_id'])
        members = self.cleaned_data['members']

        if not user_qset[0] in members:
            members = list(chain(members, user_qset))

        print(members)
        return members

    def clean_type(self):
        chat_type = 'C'
        return chat_type
