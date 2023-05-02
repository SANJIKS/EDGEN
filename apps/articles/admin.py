from django.contrib import admin
from .models import Article, Comment, Like, DisLike, Favorite, Tags


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at', 'rating')
    list_filter = ('user',)
    search_fields = ('title', 'description')

admin.site.register(Article, ArticleAdmin)
admin.site.register([Comment, Like, DisLike, Favorite, Tags])
