from django.contrib import admin
from .models import News, NewsRating, NewsComment

admin.site.register([News, NewsRating, NewsComment])