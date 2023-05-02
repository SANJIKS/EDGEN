from rest_framework import serializers
from django.db.models import Avg
from django.db import models

from .models import Article, Comment, Favorite, Like, DisLike, Tags


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Like
        fields = ('user',)


class DisLikeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = DisLike
        fields = ('user',)


class ArticleListSerializer(serializers.ListSerializer):
    def get_image_url(self, image):
        request = self.context['request']
        a = request.build_absolute_uri(image.url)
        return a

    def to_representation(self, data):
        iterable = data.all() if isinstance(data, models.Manager) else data
        return [{
            'slug': item.slug,
            'title': item.title,
            'user': item.user.username,
            'image_url': self.get_image_url(item.image) if item.image else None,
        } for item in iterable]


class ArticleSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(method_name='get_likes_count')

    class Meta:
        model = Article
        exclude = ['rating']
        read_only_fields = ['user', 'rating', 'slug']
        list_serializer_class = ArticleListSerializer

    def get_likes_count(self, instance) -> int:
        return Like.objects.filter(article=instance).count()

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['liked_users'] = LikeSerializer(
            instance.likes.all(), many=True).data
        representation['comments'] = CommentSerializer(
            instance.comments.all(), many=True).data
        return representation


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = '__all__'
        read_only_fields = ['slug']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['articles'] = [
            {'title': article.title, 'slug': article.slug} for article in instance.articles.all()]
        return representation


class FavoriteSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Favorite
        fields = ('user', 'article')


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        fields = ('id', 'user', 'article', 'text', 'created_at')
        read_only_fields = ['article']
