from django.http import Http404
from rest_framework import permissions, viewsets

from ..permissions import IsOwner, IsStudentOrOwner
from ..university.models import University
from ..subject.models import Subject
from .serializers import LectureSerializer


class LectureViewSet(viewsets.ModelViewSet):
    serializer_class = LectureSerializer

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return []
        try:
            university = University.objects.get(id=self.kwargs['uni_id'])
        except University.DoesNotExist:
            raise Http404('University does not exist')
        try:
            subject = university.subjects.get(id=self.kwargs['sub_id'])
        except Subject.DoesNotExist:
            raise Http404('Subject does not exist')
        return subject.lectures.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if getattr(self, 'swagger_fake_view', False):
            return context

        try:
            university = University.objects.get(id=self.kwargs['uni_id'])
        except University.DoesNotExist:
            raise Http404('University does not exist')

        try:
            subject = university.subjects.get(id=self.kwargs['sub_id'])
        except university.subjects.DoesNotExist:
            raise Http404('Subject does not exist')

        context['subject'] = subject
        return context

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return [IsOwner()]
        return [IsStudentOrOwner()]
