from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import University
from .permissions import IsOwner
from .serializers import AddOwnerSerializer, UniversitySerializer


class UniversityViewSet(viewsets.ModelViewSet):
    queryset = University.objects.all()

    def get_permissions(self):
        if self.request.method in ['GET', 'POST'] and \
           not self.action == 'add_owner':
            return [permissions.IsAuthenticatedOrReadOnly()]
        return [IsOwner()]

    def get_serializer_class(self, *args, **kwargs):
        if self.action in ('add_owner', 'remove_owner'):
            return AddOwnerSerializer
        return UniversitySerializer

    @action(['POST'], detail=True)
    def add_owner(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={
                                         'university': self.get_object()})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(['PUT'], detail=True)
    def remove_owner(self, request, *args, **kwargs):
        university = self.get_object()
        owner_pk = request.data.get('owner_pk')
        owner = self.get_object().owners.get(pk=owner_pk)
        university.owners.remove(owner)
        return Response(status=status.HTTP_204_NO_CONTENT)
