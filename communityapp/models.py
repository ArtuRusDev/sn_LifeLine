from django.db import models

from newsapp.models import NewsItem, Comments
from sn_LifeLine import settings


class Community(models.Model):
    name = models.CharField(blank=False, null=False, max_length=35, verbose_name="Название сообщества")
    image = models.ImageField(upload_to="communities_images", blank=True, default=None, verbose_name="Изображние")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, verbose_name="Создатель")
    description = models.TextField(blank=True, max_length=1024, verbose_name="Описание сообщества")
    crate_date = models.DateField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Сообщество"
        verbose_name_plural = "Сообщества"

    def __str__(self):
        return self.name


class CommunityNewsItem(models.Model):
    community = models.ForeignKey('Community', on_delete=models.CASCADE, verbose_name='Сообщество')
    text = models.TextField(blank=False, null=False, max_length=1024, verbose_name='Текст Новости')
    add_datetime = models.DateTimeField(auto_now=True, verbose_name='Дата Добавления')
    image = models.FileField(verbose_name="Изображние", upload_to='news_images', blank=True, default=None)

    class Meta:
        verbose_name = 'Новость сообщества'
        verbose_name_plural = 'Новости сообщества'
        ordering = ('-add_datetime',)

    def __str__(self):
        return f'{self.community} - {self.text[:120]}'

    @property
    def all_liker_pk(self):
        return [item.user.pk for item in self.likes.all()]

    @property
    def all_liker(self):
        return ', '.join([item.user.get_name for item in self.likes.all()])

    @property
    def all_comments(self):
        return Comments.objects.filter(news_item=self.id)
