from django.db import models
from django.utils import timezone
from sn_LifeLine import settings


class FriendRequests(models.Model):
    STATUS_CHOICES = (
        (0, "Запрошено"),
        (1, "Одобрено"),
        (2, "Не друзья"),
        (3, "Отменено"),
    )

    STATUS_DICT = {
        0: "Запрошено",
        1: "Одобрено",
        2: "Не друзья",
        3: "Отменено"
    }

    initiator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Инициатор')
    target = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='friend_target',
                               verbose_name='Получатель')
    status = models.IntegerField(verbose_name="Статус", choices=STATUS_CHOICES, default=0)
    created_at = models.DateTimeField(verbose_name='Дата запроса')
    confirmed_at = models.DateTimeField(verbose_name='Дата ответа')

    def save(self, *args, **kwargs):
        """ Обновление Даты создания и редактировния """
        if not self.id:
            self.created_at = timezone.now()
        self.confirmed_at = timezone.now()
        return super(FriendRequests, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Запрос в друзья'
        verbose_name_plural = 'Запросы в друзья'

    def __str__(self):
        return f'({self.STATUS_DICT[self.status]}) {self.initiator.username} - {self.target.username}'
