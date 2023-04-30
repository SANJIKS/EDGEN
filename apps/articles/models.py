from django.db import models
from django.contrib.auth import get_user_model
from slugify import slugify
from datetime import datetime

User = get_user_model()


class Tags(models.Model):
    slug = models.SlugField(primary_key=True, blank=True, max_length=80)
    title = models.CharField(max_length=80, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Article(models.Model):
    slug = models.SlugField(primary_key=True, max_length=150, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    tag = models.ForeignKey(Tags, on_delete=models.CASCADE,
                            related_name='articles', default='islamchik')
    image = models.ImageField(upload_to='articles', default='articles/default.jpg')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='articles')
    rating = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['created_at']

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title) + \
                datetime.now().strftime('_%d_%M_%H')
        return super().save(*args, **kwargs)


class Favorite(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='favorites')
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name='favorites')

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        unique_together = ('user', 'article')

    def __str__(self):
        return f'{self.article.title} Added to favorites by {self.user.username}'


class Comment(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name='comments')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self) -> str:
        return f'Комментарий от {self.user.username}'


class Like(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='likes')
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'
        unique_together = ('user', 'article')

    def __str__(self):
        return f'Liked by {self.user.username}'


class DisLike(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='dislikes')
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name='dislikes')

    class Meta:
        verbose_name = 'Дислайк'
        verbose_name_plural = 'Дислайк'

    def __str__(self) -> str:
        return f'Disliked by {self.user.username}'
