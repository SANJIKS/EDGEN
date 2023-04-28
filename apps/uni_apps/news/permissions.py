from rest_framework.permissions import BasePermission

from apps.uni_apps.university.models import University

class IsAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user == obj.user


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        university = University.objects.get(view['kwargs'].get('uni_id'))
        return bool(
            user.is_authenticated() and
            user in university.owners.all()
        )
