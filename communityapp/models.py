from django.db import models

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