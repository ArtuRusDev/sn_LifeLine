from django.core.management import BaseCommand

from newsapp.models import NewsItem


class Command(BaseCommand):
    def handle(self, *args, **options):
        news_list = NewsItem.objects.all()
        for news_item in news_list:
            news_item.text = news_item.text.replace('\n', '<br>')
            news_item.save()
        print('success')
