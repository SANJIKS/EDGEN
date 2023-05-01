from rest_framework import serializers
from django.db import models
from django.db.models import Avg

from apps.uni_apps.university.models import University


from .models import News, NewsRating, NewsComment

class NewsListSerializer(serializers.ListSerializer):
    def get_image_url(self, image):
        request = self.context['request']
        image_url = request.build_absolute_uri(image.url)
        return image_url

    def to_representation(self, data):
        iterable = data.all() if isinstance(data, models.Manager) else data
        return [{
            'slug': item.slug,
            'title': item.title,
            'university': item.university.name,
            'image_url': self.get_image_url(item.image) if item.image else None,
        } for item in iterable]


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'
        read_only_fields = ['university', 'slug']
        list_serializer_class = NewsListSerializer
    
    def create(self, validated_data):
        validated_data['university'] = self.context['university']
        return super().create(validated_data)


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['rating'] = instance.rating.aggregate(Avg('rate'))['rate__avg']
        representation['comments'] = NewsCommentSerializer(instance.news_comments.all(), many=True).data
        return representation
    


class NewsCommentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = NewsComment
        fields = ('id', 'user', 'news', 'text', 'created_at')
        read_only_fields = ['news']


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsRating
        fields = ('id', 'user', 'news', 'rate')
        read_only_fields = ['user', 'news']


    def validate(self, attrs):
        user = self.context.get('request').user
        news = self.context.get('news')
        rate = NewsRating.objects.filter(user=user, news=news).exists()
        if rate:
            raise serializers.ValidationError({'message': 'Rate already exists'})
        return super().validate(attrs)

    def create(self, validated_data):
        validated_data['user'] = self.context.get('request').user
        return super().create(validated_data)
