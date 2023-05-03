from rest_framework.permissions import BasePermission

from .models import Quiz


class IsOwnerOfQuiz(BasePermission):
    def has_permission(self, request, view):
            user = request.user
            quiz = Quiz.objects.get(pk=view.kwargs.get('id'))

            return bool(
                user.is_authenticated and
                user in quiz.subject.university.owners.all()
            )

    def has_object_permission(self, request, view, obj):
        return bool(
            request.user.is_authenticated and
            request.user in obj.subject.university.owners.all()
        )
