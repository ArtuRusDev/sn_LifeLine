from django.contrib import admin

# Register your models here.
from newsapp.models import NewsItem, Likes

admin.site.register(NewsItem)
admin.site.register(Likes)
