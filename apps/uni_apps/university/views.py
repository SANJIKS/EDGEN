from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import University
from .permissions import IsOwner
from .serializers import (OwnerSerializer, StudentsSerializer,
                          UniversitySerializer)


class UniversityViewSet(viewsets.ModelViewSet):
    queryset = University.objects.filter(approved=True)

    def get_permissions(self):
        if self.request.method in ['GET', 'POST'] and \
           not self.action in ('owner', 'students'):
            return [permissions.IsAuthenticatedOrReadOnly()]
        return [IsOwner()]

    def get_serializer_class(self, *args, **kwargs):
        if self.action in ('owner'):
            return OwnerSerializer
        if self.action == 'students':
            return StudentsSerializer
        return UniversitySerializer

    @action(['POST', 'PUT'], detail=True)
    def owner(self, request, *args, **kwargs):
        if request.method == 'POST':
            serializer = self.get_serializer(data=request.data, context={
                                             'university': self.get_object(),
                                             'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == 'PUT':
            university = self.get_object()
            serializer = self.get_serializer(university, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(['PUT', 'POST'], detail=True)
    def students(self, request, *args, **kwargs):
        if request.method == 'POST':
            serializer = self.get_serializer(data=request.data, context={
                                             'university': self.get_object(),
                                             'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == 'PUT':
            university = self.get_object()
            serializer = self.get_serializer(university, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
