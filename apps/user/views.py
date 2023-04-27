from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from djoser import signals, utils
from djoser.conf import settings as djoser_settings
from djoser.views import UserViewSet
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from .models import Profile
from .permissions import IsAuthorOrReadOnly
from .serializers import ProfileSerializer
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

        try:
            return user.profile
        except Profile.DoesNotExist:
            return Profile.objects.create(user=user)

    @action(["get", "put", "patch", "delete"], detail=False)
    def me(self, request, *args, **kwargs):
        if request.method == "PUT":
            return self.update(request, *args, **kwargs)
        elif request.method == "PATCH":
            return self.partial_update(request, *args, **kwargs)
