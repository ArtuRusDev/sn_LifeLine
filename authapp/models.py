from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from friendsapp.models import FriendRequests

GENDER_CHOICES = [
    ['male', "Мужской"],
    ['female', "Женский"]
]

GENDER_DICT = {
    'male': "Мужской",
    'female': "Женский"
}

REL_DICT = {
    0: "Не определенно",
    1: "Холост",
    2: "В отношениях",
    3: "Помолвлен(а)",
    4: "Женат/Замужем",
    5: "Влюблен(а)",
    6: "Все сложно",
}


class Person(AbstractUser):
    STATUS_CHOICES = (
        (0, "Не определенно"),
        (1, "Холост"),
        (2, "В отношениях"),
        (3, "Помолвлен(а)"),
        (4, "Женат/Замужем"),
        (5, "Влюблен(а)"),
        (6, "Все сложно"),
    )
    patronymic = models.CharField(max_length=30, blank=True, verbose_name="Отчество")
    avatar = models.FileField(upload_to='users_avatars', blank=True, default=None, verbose_name="Аватарка")
    phone_number = PhoneNumberField(null=True, blank=True, unique=True, verbose_name="Номер телефона")
    bio = models.TextField(max_length=500, blank=True, null=True, verbose_name="О себе")
    city = models.CharField(max_length=30, blank=True, null=True, verbose_name="Город")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Дата рождения")
    gender = models.CharField(max_length=10, blank=True, null=True, default=None, choices=GENDER_CHOICES, verbose_name="Пол")
    relationship = models.IntegerField(choices=STATUS_CHOICES, default=0, verbose_name="Статус отношений")
    is_dark_theme = models.BooleanField(default=False, verbose_name="Использовать темную тему")

    @property
    def get_friends(self):
        """ Вернет Person QuerySet друзей пользователя """
        user = Person.objects.get(pk=self.pk)
        # Все подтвержденные запросы в друзья пользовалю и от него
        all_requests = FriendRequests.objects.filter(status=1, initiator=user) | \
                       FriendRequests.objects.filter(status=1, target=user)

        friends = []
        for item in all_requests:
            if item.target == user:
                friends.append(item.initiator)
            else:
                friends.append(item.target)

        return friends

    @property
    def get_friend_requests(self):
        """ Return Person QuerySet of unconfirmed friends request TO user """
        user = Person.objects.get(pk=self.pk)
        all_requests = FriendRequests.objects.filter(status=0, target=user)

        friends_pk = [item.initiator.pk for item in all_requests]

        result = Person.objects.filter(pk__in=friends_pk)
        return result

    @property
    def get_send_friend_requests_pk(self):
        """ Return list of users' pk which user send friends request  """

        user = Person.objects.get(pk=self.pk)
        all_requests = FriendRequests.objects.filter(status=0, initiator=user)
        friends_pk = [item.target.pk for item in all_requests]

        return friends_pk

    @property
    def get_name(self):
        if self.patronymic:
            return f'{self.last_name} {self.first_name} {self.patronymic}'
        elif self.first_name:
            return f'{self.first_name} {self.last_name}'
        return self.username

    @property
    def get_gender(self):
        return GENDER_DICT.get(self.gender)

    @property
    def get_rel(self):
        if self.relationship == 0:
            return False
        return REL_DICT.get(self.relationship)
