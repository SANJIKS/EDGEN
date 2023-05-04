from rest_framework import serializers
from .models import Subject, Skill
from ..material.serializers import LectureSerializer


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'
        read_only_fields = ['university']

    def create(self, validated_data):
        validated_data['university'] = self.context['university']
        return super().create(validated_data)

    def to_representation(self, instance):
        repr_ = super().to_representation(instance)
        repr_['lectures'] = LectureSerializer(instance.lectures.all(), many=True).data
        return repr_


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'
        read_only_fields = ['slug']
