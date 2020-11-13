from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from authapp.models import Person


class Chat(models.Model):
    DIALOG = 'D'
    CHAT = 'C'
    CHAT_TYPE_CHOICES = (
        (DIALOG, 'Dialog'),
        (CHAT, 'Chat')
    )

    type = models.CharField(max_length=1, choices=CHAT_TYPE_CHOICES, default=DIALOG, verbose_name='Тип')
    members = models.ManyToManyField(Person, verbose_name="Участник", blank=False)

    # @models.permalink
    def get_absolute_url(self):
        return 'users:messages', (), {'chat_id': self.pk}


class Message(models.Model):
    chat = models.ForeignKey(Chat, verbose_name="Чат", on_delete=models.CASCADE)
    author = models.ForeignKey(Person, verbose_name="Пользователь", on_delete=models.DO_NOTHING)
    message = models.TextField("Сообщение")
    pub_date = models.DateTimeField('Дата сообщения', default=timezone.now)
    is_read = models.BooleanField('Прочитано', default=False)

    class Meta:
        ordering = ['pub_date']

    def __str__(self):
        return self.message
