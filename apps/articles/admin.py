from django.contrib import admin
from .models import Article, Comment, Like, DisLike, Favorite

admin.site.register([Article, Comment, Like, DisLike, Favorite])
