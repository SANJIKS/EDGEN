from djoser.views import UserViewSet
from djoser.compat import get_user_email
from djoser import signals, utils
from django.contrib.auth.tokens import default_token_generator


from .tasks import send_activation_email
from rest_framework.response import Response
from rest_framework import status


class CustomUserViewSet(UserViewSet):
    """
    Custom user view set, inherited from djoser UserViewSet
    """

    def perform_create(self, serializer, *args, **kwargs):
        user = serializer.save(*args, **kwargs)
        signals.user_registered.send(
            sender=self.__class__, user=user, request=self.request
        )

        context = {}

        context["uid"] = utils.encode_uid(user.pk)
        context["token"] = default_token_generator.make_token(user)

        send_activation_email.delay(user.pk, context)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
