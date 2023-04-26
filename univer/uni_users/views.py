from rest_framework import generics, permissions
from .models import OrganizationRegistration
from .serializers import OrganizationRegistrationSerializer

class OrganizationRegistrationList(generics.ListCreateAPIView):
    queryset = OrganizationRegistration.objects.all().exclude(approved=True)
    serializer_class = OrganizationRegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]

    

class OrganizationRegistrationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrganizationRegistration.objects.all()
    serializer_class = OrganizationRegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]
