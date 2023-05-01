from django.db import models
from rest_framework import serializers

from .models import Lecture, LectureFile


class LectureFileSerialzer(serializers.ModelSerializer):
    class Meta:
        model = LectureFile
        fields = ['file']


class LectureListSerialzer(serializers.ListSerializer):

    def to_representation(self, data):
        iterable = data.all() if isinstance(data, models.Manager) else data

        return [{
            'id': item.id,
            'title': item.title,
            'description': item.description,
        } for item in iterable]


class LectureSerializer(serializers.ModelSerializer):
    lecture_files = serializers.ListField(
        child=serializers.FileField(),
        write_only=True,
        required=False
    )
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Lecture
        fields = '__all__'
        read_only_fields = ['subject', 'user']
        list_serializer_class = LectureListSerialzer

    def create(self, validated_data):
        validated_data['subject'] = self.context['subject']
        validated_data['user'] = self.context['request'].user
        lecture_files = validated_data.pop('lecture_files')
        lecture = Lecture.objects.create(**validated_data)

        if lecture_files:
            files = [LectureFile(lecture=lecture,
                                 file=file) for file in lecture_files]

            LectureFile.objects.bulk_create(files)

        return lecture

    def to_representation(self, instance):
        representaion = super().to_representation(instance)

        representaion['files'] = LectureFileSerialzer(
            instance.files.all(), many=True).data

        return representaion
