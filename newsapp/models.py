from django.db import models

# Create your models here.
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
