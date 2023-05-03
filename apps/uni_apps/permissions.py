from rest_framework.permissions import BasePermission

from .university.models import University
from .subject.models import Subject


class IsOwner(BasePermission):
    def has_permission(self, request, view):
        if view.request.method == 'POST':
            user = request.user
            university = University.objects.get(pk=view.kwargs.get('id'))

            return bool(
                user.is_authenticated and
                user in university.owners.all()
            )
        return True

    def has_object_permission(self, request, view, obj):
        return bool(
            request.user.is_authenticated and
            request.user in obj.university.owners.all()
        )


class IsStudentOrOwner(BasePermission):
    def has_permission(self, request, view):
        if view.action in ('create', 'list'):
            user = request.user
            university = University.objects.get(pk=view.kwargs.get('id'))
            return bool(
                user.is_authenticated and
                (user in university.students.all() or
                 user in university.owners.all())
            )
        return True

    def has_object_permission(self, request, view, obj):
        return bool(
            request.user.is_authenticated and
            (request.user in obj.university.owners.all() or
             request.user in obj.university.students.all())
        )


class IsOwnerOfSubject(BasePermission):
    def has_permission(self, request, view):
        if view.request.method == 'POST':
            user = request.user
            subject = Subject.objects.get(pk=view.kwargs.get('id'))

            return bool(
                user.is_authenticated and
                user in subject.university.owners.all()
            )
        return True

    def has_object_permission(self, request, view, obj):
        return bool(
            request.user.is_authenticated and
            request.user in obj.university.owners.all()
        )


class IsStudentOrOwnerOfSubject(BasePermission):
    def has_permission(self, request, view):
        if view.action in ('create', 'list'):
            user = request.user
            subject = Subject.objects.get(pk=view.kwargs.get('id'))
            return bool(
                user.is_authenticated and
                (user in subject.university.students.all() or
                 user in subject.university.owners.all())
            )
        return True

    def has_object_permission(self, request, view, obj):
        return bool(
            request.user.is_authenticated and
            (request.user in obj.subject.university.owners.all() or
             request.user in obj.subject.university.students.all())
        )
