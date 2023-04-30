from rest_framework import serializers
from .models import Subject


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'
        read_only_fields = ['university']

    def create(self, validated_data):
        validated_data['university'] = self.context['university']
        return super().create(validated_data)
