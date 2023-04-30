from rest_framework.permissions import BasePermission

from .university.models import University


class IsOwner(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        university = University.objects.get(pk=view.kwargs.get('uni_id'))
        return bool(
            user.is_authenticated and
            user in university.owners.all()
        )
