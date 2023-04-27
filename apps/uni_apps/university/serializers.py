from rest_framework import serializers

from .models import University


class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        exclude = ('owners', 'approved', 'students')

    def create(self, validated_data):
        validated_data['owners'] = [self.context['request'].user]
        return super().create(validated_data)


class AddOwnerSerializer(serializers.Serializer):
    owner = serializers.IntegerField()
    university = serializers.RelatedField(read_only=True)

    def valida_user(self, owner):
        if not owner.is_active:
            raise serializers.ValidationError('User must be active')
        return owner

    def create(self, validated_data):
        university = self.context['university']
        print(validated_data)
        university.owners.add(validated_data['owner'])
        university.save()
        return university

    def to_representation(self, instance):
        repr_ = {
            'owner': instance.owners.last().username
        }
        return repr_
