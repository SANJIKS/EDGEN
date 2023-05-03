from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from ..permissions import IsOwnerOfSubject, IsStudentOrOwnerOfSubject
from ..subject.models import Subject
from .models import Question, Quiz
from .permissions import IsOwnerOfQuiz
from .serializers import (GetResultSerializer, QuestionSerializer,
                          QuizSerializer)


class QuizList(mixins.CreateModelMixin,
               mixins.ListModelMixin,
               viewsets.GenericViewSet):
    serializer_class = QuizSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [IsOwnerOfSubject()]
        return [IsStudentOrOwnerOfSubject()]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if getattr(self, 'swagger_fake_view', False):
            return context

        subject = get_object_or_404(Subject, id=self.kwargs.get('id'))
        context.update({'subject': subject})
        return context

    def get_queryset(self):
        subject_id = self.kwargs.get('id')
        return Quiz.objects.filter(subject_id=subject_id)


class QuizDetail(mixins.RetrieveModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin,
                 viewsets.GenericViewSet):
    queryset = Quiz.objects.all()

    def get_serializer_class(self):
        if self.action == 'result':
            return GetResultSerializer
        return QuizSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if getattr(self, 'swagger_fake_view', False):
            return context

        if self.action == 'result':
            quiz = get_object_or_404(Quiz, id=self.kwargs.get('id'))
            context.update({'quiz': quiz})
        return context

    def get_permissions(self):
        if self.action == 'retrieve':
            return [IsStudentOrOwnerOfSubject()]
        return [IsOwnerOfSubject()]

    @action(['POST'], detail=True)
    def result(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)


class QuestionList(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    serializer_class = QuestionSerializer
    permission_classes = [IsOwnerOfQuiz]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if getattr(self, 'swagger_fake_view', False):
            return context

        quiz = get_object_or_404(Quiz, id=self.kwargs.get('id'))
        context.update({'quiz': quiz})
        return context
    
    def get_queryset(self):
        quiz_id = self.kwargs.get('id')
        return Question.objects.filter(quiz_id=quiz_id)


class QuestionDetail(mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsOwnerOfQuiz]
