from django.contrib import admin

# Register your models here.
from newsapp.models import NewsItem

admin.site.register(NewsItem)
