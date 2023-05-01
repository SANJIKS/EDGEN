from django.contrib.auth import get_user_model
from django.db import models
from rest_framework import serializers

from apps.user.serializers import CustomUserSerializer

from .models import University
from .tasks import (send_owner_add, send_owner_delete, send_student_inroll,
                    send_student_outroll)



User = get_user_model()


class UniversityListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        iterable = data.all() if isinstance(data, models.Manager) else data

        return [{
            'id': item.id,
            'name': item.name,
            'address': item.address,
            'avatar': item.avatar.url if item.avatar else None
        } for item in iterable]


class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        exclude = ('owners', 'approved', 'students')
        list_serializer_class = UniversityListSerializer

    def create(self, validated_data):
        validated_data['owners'] = [self.context['request'].user]
        return super().create(validated_data)

    def to_representation(self, instance):
        repr_ = super().to_representation(instance)
        repr_['owners'] = CustomUserSerializer(
            instance.owners.all(), many=True).data
        repr_['students'] = CustomUserSerializer(
            instance.students.all(), many=True).data
        return repr_


class OwnerSerializer(serializers.Serializer):
    owner = serializers.IntegerField()

    def validate_owner(self, owner):
        request = self.context['request']

        if request.method == 'POST':
            if self.context['university'].owners.filter(pk=owner).exists():
                raise serializers.ValidationError('User already owner')

        elif request.method == 'PUT':
            if not self.instance.owners.filter(pk=owner).exists():
                raise serializers.ValidationError('User not owner')

        if not User.objects.filter(pk=owner).exists():
            raise serializers.ValidationError('User not found')

        return owner

    def create(self, validated_data):
        university = self.context['university']
        owner = User.objects.get(pk=validated_data['owner'])
        university.owners.add(owner)
        university.save()
        send_owner_add.delay(owner.email, university.name)
        return university

    def update(self, instance, validated_data):
        owner_pk = validated_data.get('owner')
        owner = instance.owners.get(pk=owner_pk)
        instance.owners.remove(owner)
        instance.save()
        send_owner_delete.delay(owner.email, instance.name)
        return instance

    def to_representation(self, instance):
        repr_ = {
            'owner': instance.owners.last().username,
        }
        return repr_


class StudentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = ('students',)

    def validate_students(self, students):
        request = self.context['request']

        if request.method == 'POST':
            for student in students:
                if self.context['university'].students.filter(pk=student.pk).exists():
                    raise serializers.ValidationError('User already student')

        elif request.method == 'PUT':
            for student in students:
                if not self.instance.students.filter(pk=student.pk).exists():
                    raise serializers.ValidationError('User not student')

        for student in students:
            if not User.objects.filter(pk=student.pk).exists():
                raise serializers.ValidationError('User not found')

        return students

    def create(self, validated_data):
        university = self.context['university']
        recipient_list = []
        for student in validated_data['students']:
            user = User.objects.get(pk=student.id)
            university.students.add(user)
            recipient_list.append(user.email)
        university.save()
        send_student_inroll.delay(recipient_list, university.name)
        return university

    def update(self, instance, validated_data):
        recipient_list = []
        for student in validated_data['students']:
            user = User.objects.get(pk=student.id)
            instance.students.remove(user)
            recipient_list.append(user.email)
        instance.save()
        send_student_outroll.delay(recipient_list, instance.name)
        return instance

    def to_representation(self, instance):
        students = [CustomUserSerializer(
            student).data for student in instance.students.all()]
        repr_ = {
            'students': students
        }
        return repr_
