from rest_framework import permissions, viewsets

from apps.uni_apps.university.models import University

from ..permissions import IsOwner
from .models import Subject
from .serializers import SubjectSerializer


class SubjectViewSet(viewsets.ModelViewSet):
    serializer_class = SubjectSerializer

    def get_queryset(self):
        uni_id = self.kwargs.get('uni_id')
        return Subject.objects.filter(university=uni_id)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if getattr(self, 'swagger_fake_view', False):
            return context
        uni_id = self.kwargs.get('uni_id')
        context['university'] = University.objects.get(pk=uni_id)
        return context

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return [IsOwner()]
        return [permissions.AllowAny()]
