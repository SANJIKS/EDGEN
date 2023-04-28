from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.user.serializers import CustomUserSerializer

from .models import University
from .tasks import (send_owner_add, send_owner_delete, send_student_inroll,
                    send_student_outroll)

User = get_user_model()


class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        exclude = ('owners', 'approved', 'students')

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
        if not owner.is_active:
            raise serializers.ValidationError('User must be active')
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
        try:
            owner = instance.owners.get(pk=owner_pk)
        except instance.owners.model.DoesNotExist:
            raise serializers.ValidationError({'owner': 'Owner not found'})
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

    def create(self, validated_data):
        university = self.context['university']
        recipient_list = []
        for student in validated_data['students']:
            try:
                user = User.objects.get(pk=student.id)
            except User.DoesNotExist:
                raise serializers.ValidationError({'students': 'User not found'})
            university.students.add(user)
            recipient_list.append(user.email)
        university.save()
        send_student_inroll.delay(recipient_list, university.name)
        return university

    def update(self, instance, validated_data):
        recipient_list = []
        for student in validated_data['students']:
            try:
                user = User.objects.get(pk=student.id)
            except User.DoesNotExist:
                raise serializers.ValidationError({'students': 'User not found'})
            instance.students.remove(user)
            recipient_list.append(user.email)
        instance.save()
        send_student_outroll.delay(recipient_list, instance.name)
        return instance
    
    def to_representation(self, instance):
        students = [CustomUserSerializer(student).data for student in instance.students.all()]
        repr_ = {
            'students': students
        }
        return repr_