from django.db import models

from newsapp.models import NewsItem
from sn_LifeLine import settings


class Community(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Создатель")
    name = models.CharField(blank=False, null=False, max_length=35, verbose_name="Название сообщества")
    image = models.ImageField(upload_to="communities_images", blank=True, default=None, verbose_name="Изображние")
    description = models.TextField("Описание сообщества", blank=True, max_length=1024)
    crate_date = models.DateField("Дата создания", auto_now_add=True)

    class Meta:
        verbose_name = "Сообщество"
        verbose_name_plural = "Сообщества"

    def __str__(self):
        return self.name

    @property
    def get_publishers_id(self):
        all_publishers = CommunityParticipant.objects.filter(community_id=self.id, role=1)
        return [instance.user_id for instance in all_publishers] + [self.creator.id]

    @property
    def get_subscribers_id(self):
        all_subscribers = CommunityParticipant.objects.filter(community_id=self.id)
        return [instance.user_id for instance in all_subscribers]


class CommunityNewsItem(NewsItem):
    community = models.ForeignKey(Community, on_delete=models.CASCADE, verbose_name='Сообщество')

    class Meta:
        verbose_name = 'Новость сообщества'
        verbose_name_plural = 'Новости сообщества'
        ordering = ('-add_datetime',)


class CommunityParticipant(models.Model):
    ROLE_CHOICES = (
        (0, "Подписчик"),
        (1, "Публикатор"),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Участник')
    community = models.ForeignKey(Community, on_delete=models.CASCADE, verbose_name='Сообщество')
    role = models.IntegerField('Роль в сообществе', choices=ROLE_CHOICES, default=0, blank=False)

    class Meta:
        verbose_name = 'Участник сообщества'
        verbose_name_plural = 'Участники сообщества'
