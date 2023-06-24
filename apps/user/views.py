from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.dispatch import receiver
from django.shortcuts import get_object_or_404
from djoser import signals, utils
from djoser.conf import settings as djoser_settings
from djoser.views import UserViewSet
from rest_framework import generics, mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from .models import Profile, Subscription
from .permissions import IsAuthorOrReadOnly
from .serializers import ProfileSerializer, SubscriptionSerializer
from .tasks import send_registration, send_reset_password, send_reset_username

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    """
    Custom user view set, inherited from djoser UserViewSet
    """

    def perform_create(self, serializer, *args, **kwargs):
        user = serializer.save(*args, **kwargs)
        signals.user_registered.send(
            sender=self.__class__, user=user, request=self.request
        )

        context = {
            'uid': utils.encode_uid(user.pk),
            'token': default_token_generator.make_token(user),
            'domain': self.request.build_absolute_uri('/')
        }

        send_registration.delay(user.pk, context)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(["post"], detail=False)
    def resend_activation(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.get_user(is_active=False)

        if not djoser_settings.SEND_ACTIVATION_EMAIL or not user:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        context = {
            'uid': utils.encode_uid(user.pk),
            'token': default_token_generator.make_token(user),
            'domain': self.request.build_absolute_uri('/')
        }

        send_registration.delay(user.pk, context)

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(["post"], detail=False)
    def reset_password(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.get_user()

        if user:
            context = {
                'uid': utils.encode_uid(user.pk),
                'token': default_token_generator.make_token(user),
                'domain': self.request.build_absolute_uri('/')
            }

            send_reset_password.delay(user.pk, context)

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(["post"], detail=False, url_path=f"reset_{User.USERNAME_FIELD}")
    def reset_username(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.get_user()

        if user:
            context = {
                'uid': utils.encode_uid(user.pk),
                'token': default_token_generator.make_token(user),
                'domain': self.request.build_absolute_uri('/')
            }
            send_reset_username.delay(user.pk, context)

        return Response(status=status.HTTP_204_NO_CONTENT)


class ProfileViewSet(mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     viewsets.GenericViewSet):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthorOrReadOnly]
    queryset = Profile.objects.all()
    parser_classes = [MultiPartParser]

    def get_object(self):

        if self.action == 'me':
            user = self.request.user
        else:
            user_id = self.kwargs['id']
            user = User.objects.get(pk=user_id)
        self.check_object_permissions(self.request, user)

        return user.profile

    @action(["put", "patch"], detail=False)
    def me(self, request, *args, **kwargs):
        if request.method == "PUT":
            return self.update(request, *args, **kwargs)
        elif request.method == "PATCH":
            return self.partial_update(request, *args, **kwargs)


class SubscriptionViewSet(mixins.CreateModelMixin,
                          mixins.DestroyModelMixin,
                          viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SubscriptionSerializer

    def get_object(self):
        subscribed_to = get_object_or_404(User, id=self.kwargs['id'])
        return get_object_or_404(Subscription, subscriber=self.request.user, subscribed_to=subscribed_to)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if getattr(self, 'swagger_fake_view', False):
            return context

        context['subscribed_to'] = self.kwargs['id']
        return context

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SubscriptionListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SubscriptionSerializer

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return Subscription.objects.none()
        return Subscription.objects.filter(subscriber=self.request.user)
