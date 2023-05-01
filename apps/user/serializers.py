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
    class Meta:
        model = Subscription
        fields = '__all__'
        read_only_fields = ['subscriber', 'subscribed_to']

    def validate(self, attrs):
        request = self.context['request']
        attrs['subscriber'] = request.user
        sub_to_id = self.context['subscribed_to']

        try:
            attrs['subscribed_to'] = User.objects.get(id=sub_to_id)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                f"User with id {sub_to_id} does not exist")

        if (request.method == 'POST' and
                attrs['subscriber'] == attrs['subscribed_to']):
            raise serializers.ValidationError(
                "You cannot subscribe to yourself")
        return attrs

    def to_representation(self, instance):
        repr_ = super().to_representation(instance)
        repr_['subscriber'] = instance.subscriber.username  # TODO
        repr_['subscribed_to'] = instance.subscribed_to.username
        return repr_
