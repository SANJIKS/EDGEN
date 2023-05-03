from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets

from ..permissions import IsOwnerOfSubject, IsStudentOrOwnerOfSubject
from ..subject.models import Subject
from .models import Lecture
from .serializers import LectureSerializer


class LectureList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  viewsets.GenericViewSet):
    serializer_class = LectureSerializer

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return []
        subject = get_object_or_404(Subject, id=self.kwargs['id'])
        return subject.lectures.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if getattr(self, 'swagger_fake_view', False):
            return context
        context['subject'] = get_object_or_404(Subject, id=self.kwargs['id'])
        return context

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsOwnerOfSubject()]
        return [IsStudentOrOwnerOfSubject()]


class LectureDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    serializer_class = LectureSerializer
    queryset = Lecture.objects.all()

    def get_permissions(self):
        if self.request.method in ('PUT', 'PATCH', 'DELETE'):
            return [IsOwnerOfSubject()]
        return [IsStudentOrOwnerOfSubject()]
