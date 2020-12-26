from django.conf import settings
from django.core.management.base import BaseCommand

from authapp.models import Person
from newsapp.models import NewsItem, Likes
from friendsapp.models import FriendRequests
from messengerapp.models import Chat, Message

import json
import os

JSON_PATH = os.path.join(settings.BASE_DIR, 'mainapp/json')


def load_from_json(file_name):
    with open(os.path.join(JSON_PATH, file_name + '.json'), 'r', encoding='utf-8') as json_file:
        print(f'{file_name}.json - OK')
        return json.load(json_file)


class Command(BaseCommand):
    def handle(self, *args, **options):
        users = load_from_json('users')
        Person.objects.all().delete()
        for user in users:
            Person.objects.create(**user)

        news = load_from_json('news')
        NewsItem.objects.all().delete()
        for item_item in news:
            NewsItem.objects.create(**item_item)

        likes = load_from_json('likes')
        Likes.objects.all().delete()
        for like in likes:
            Likes.objects.create(**like)

        requests = load_from_json('friends')
        FriendRequests.objects.all().delete()
        for request in requests:
            FriendRequests.objects.create(**request)
