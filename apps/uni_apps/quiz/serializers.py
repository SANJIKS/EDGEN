from django.shortcuts import get_object_or_404
from rest_framework import serializers

from .models import Answer, Question, Quiz


class GetResultSerializer(serializers.Serializer):
    result = serializers.IntegerField(read_only=True)
    answers = serializers.ListField()
    quiz = serializers.IntegerField(read_only=True)
    passed = serializers.BooleanField(default=False, read_only=True)

    def get_question_count(self, quiz):
        return quiz.questions.count()

    def validate(self, attrs):
        quiz = self.context['quiz']
        student = self.context['request'].user
        counter = 0

        for answer_id in attrs['answers']:
            answer = get_object_or_404(Answer, id=answer_id)
            if answer.is_correct:
                counter += 1
        question_count = self.get_question_count(quiz)
        attrs['result'] = counter / question_count * 100
        if attrs['result'] >= 60:
            for skill in quiz.subject.skills.all():
                print(skill)
                if skill not in student.profile.skills.all():
                    student.profile.skills.add(skill)
            student.profile.save()
            attrs['passed'] = True

        return attrs


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        exclude = ('question',)


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = ('id', 'text', 'answers')

    def validate_answers(self, answers):
        if len(answers) > 4:
            raise serializers.ValidationError('Answers count must less than 4')

        if len([answer for answer in answers if answer['is_correct']]) != 1:
            raise serializers.ValidationError('Only one correct answer')

        return answers

    def validate(self, attrs):
        attrs['quiz'] = self.context['quiz']
        return attrs

    def create(self, validated_data):
        answers = validated_data.pop('answers')
        question = Question.objects.create(**validated_data)
        for answer in answers:
            Answer.objects.create(question=question, **answer)

        return question

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['answers'] = AnswerSerializer(
            instance.answers.all(), many=True).data
        return representation


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        exclude = ('subject',)

    def validate(self, attrs):
        attrs['subject'] = self.context['subject']
        return attrs
    
    def to_representation(self, instance):
        repr_ = super().to_representation(instance)
        repr_['questions'] = QuestionSerializer(instance.questions.all(), many=True).data
        return repr_
