from django.contrib import admin
from .models import Article, Comment, Like, DisLike, Favorite, Tags

admin.site.register([Article, Comment, Like, DisLike, Favorite, Tags])
