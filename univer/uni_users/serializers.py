from rest_framework import serializers
from .models import OrganizationRegistration

class OrganizationRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationRegistration
        exclude = ('approved',)