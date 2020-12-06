from django.db import models

# Create your models here.
from authapp.models import Person
from sn_LifeLine import settings


class NewsItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    text = models.TextField(blank=False, null=False, max_length=1024, verbose_name='Текст Новости')
    add_datetime = models.DateTimeField(auto_now_add=True, verbose_name='Дата Добавления')
    image = models.FileField(verbose_name="Изображние", upload_to='news_images', blank=True, default=None)

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ('-add_datetime',)

    def __str__(self):
        return f'{self.user} - {self.text[:30]}'

    @property
    def all_liker_pk(self):
        return [item.user.pk for item in self.likes.all()]

    @property
    def all_liker(self):
        return ', '.join([item.user.get_name for item in self.likes.all()])


class Likes(models.Model):
    user = models.ForeignKey(Person, on_delete=models.CASCADE, verbose_name='Пользователь')
    news_item = models.ForeignKey(NewsItem, on_delete=models.CASCADE, verbose_name='Запись', related_name='likes')

    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'
