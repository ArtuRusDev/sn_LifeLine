from django.db import models
from authapp.models import Person
from sn_LifeLine import settings


class NewsItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Пользователь', on_delete=models.CASCADE)
    text = models.TextField('Текст Новости', max_length=1024)
    add_datetime = models.DateTimeField('Дата Добавления', auto_now=True)
    image = models.FileField("Изображение", upload_to='news_images', null=True, blank=True, default=None)
    is_community = models.BooleanField('Новость сообщества', default=False)
    is_moderated = models.BooleanField('Проверено модераторами', default=False)
    is_accepted = models.BooleanField('Публикация принята', default=False)

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ('-add_datetime',)

    def __str__(self):
        return f'{self.user} - {self.text[:120]}'

    @property
    def all_liker_pk(self):
        return [item.user.pk for item in self.likes.all()]

    @property
    def all_liker(self):
        return ', '.join([item.user.get_name for item in self.likes.all()])

    @property
    def all_comments(self):
        return Comments.objects.filter(news_item=self.id)


class Likes(models.Model):
    user = models.ForeignKey(Person, on_delete=models.CASCADE, verbose_name='Пользователь')
    news_item = models.ForeignKey(NewsItem, on_delete=models.CASCADE, verbose_name='Запись', related_name='likes')

    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'


class Comments(models.Model):
    news_item = models.ForeignKey(NewsItem, on_delete=models.CASCADE, verbose_name='Комментируемая новость')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Автор')
    text = models.TextField('Текст комментария', blank=False, null=False, max_length=1024)
    add_datetime = models.DateTimeField('Дата комментирования', auto_now_add=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
