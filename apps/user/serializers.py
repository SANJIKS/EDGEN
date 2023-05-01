from djoser.serializers import UserSerializer, UserCreateSerializer
from rest_framework import serializers
from .models import Profile
from rest_framework import serializers
from .models import Subscription
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Subscription



class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        exclude = ['user']


class CustomUserSerializer(UserSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ('profile',)

    def to_representation(self, instance):
        repr_ = super().to_representation(instance)
        repr_['profile'] = ProfileSerializer(instance.profile).data
        return repr_


class CustomUserCreateSerializer(UserCreateSerializer):

    class Meta(UserCreateSerializer.Meta):
        fields = UserCreateSerializer.Meta.fields

    def create(self, validated_data):
        user = super().create(validated_data)
        Profile.objects.create(user=user)
        return user

class SubscriptionSerializer(serializers.ModelSerializer):
    subscribed_to = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())

    class Meta:
        model = Subscription
        fields = ('id', 'subscriber', 'subscribed_to', 'created_at',)
        read_only_fields = ('id', 'subscriber', 'created_at',)

    def create(self, validated_data):
        subscribed_to = validated_data['subscribed_to']
        subscriber = self.context['request'].user
        if subscribed_to == subscriber:
            raise serializers.ValidationError("You cannot subscribe to yourself")
        subscription, created = Subscription.objects.get_or_create(subscriber=subscriber, subscribed_to=subscribed_to)
        if not created:
            raise serializers.ValidationError("You already subscribed to this user")
        return subscription

    def delete(self, instance):
        instance.delete()
        return instance