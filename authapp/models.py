from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

GENDER_CHOICES = [
    ['male', "Мужской"],
    ['female', "Женский"]
]

GENDER_DICT = {
    'male': "Мужской",
    'female': "Женский"
}

REL_CHOICES = [
    ['none', "Не определенно"],
    ['single', "Холост"],
    ['in_a_rel', "В отношениях"],
    ['engaged', "Помолвлен(а)"],
    ['married', "Женат/Замужем"],
    ['in_love', "Влюблен(а)"],
    ['complicated', "Все сложно"],
]


class Person(AbstractUser):
    avatar = models.FileField(verbose_name="Аватарка", null=True, blank=True)
    phone_number = PhoneNumberField(null=True, blank=True, unique=True)
    bio = models.TextField(max_length=500, blank=True, null=True, verbose_name="О себе")
    city = models.CharField(max_length=30, blank=True, null=True, verbose_name="Город")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Дата рождения")
    gender = models.CharField(max_length=10, verbose_name="Пол", choices=GENDER_CHOICES, default="male")
    relationship = models.CharField(max_length=20, verbose_name="Статус отношений", choices=REL_CHOICES,
                                    default="none")

    @property
    def get_gender(self):
        return GENDER_DICT.get(self.gender)
