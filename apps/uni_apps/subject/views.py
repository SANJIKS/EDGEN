from django.shortcuts import get_object_or_404
from rest_framework import mixins, permissions, viewsets

from ..permissions import IsOwner, IsStudentOrOwner
from ..university.models import University
from .models import Skill,  Subject
from .serializers import SkillSerializer, SubjectSerializer


class SubjectList(mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    serializer_class = SubjectSerializer

    def get_queryset(self):
        id = self.kwargs.get('id')
        return Subject.objects.filter(university=id)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if getattr(self, 'swagger_fake_view', False):
            return context
        context['university'] = get_object_or_404(
            University, id=self.kwargs.get('id'))
        return context

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsOwner()]
        return [IsStudentOrOwner()]


class SubjectDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    serializer_class = SubjectSerializer
    queryset = Subject.objects.all()

    def get_permissions(self):
        if self.request.method in ('PUT', 'PATCH', 'DELETE'):
            return [IsOwner()]
        return [IsStudentOrOwner()]


class SkillReadCreateDeleteView(mixins.CreateModelMixin,
                                mixins.DestroyModelMixin,
                                mixins.ListModelMixin,
                                viewsets.GenericViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer

    def get_permissions(self):
        method = self.request.method
        if method in permissions.SAFE_METHODS:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]
