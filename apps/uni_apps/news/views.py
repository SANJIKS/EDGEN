from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, mixins, permissions, viewsets

from .models import News, NewsRating, NewsComment
from .serializers import NewsSerializer, NewsCommentSerializer, RatingSerializer
from .permissions import IsAuthor, IsOwner
from apps.uni_apps.university.models import University


class NewsViewSet(ModelViewSet):
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['title', 'description']

    def get_permissions(self):
        if self.request.method == ['POST', 'PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [IsOwner]
        return super().get_permissions()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if getattr(self, 'swagger_fake_view', False):
            return {'request': self.request}

        try:
            university = University.objects.get(pk=self.kwargs.get('uni_id'))
        except University.DoesNotExist:
            raise Http404

        context.update({
            'request': self.request,
            'university': university
        })
        return context

    def get_queryset(self):
        return News.objects.filter(university=self.kwargs.get('uni_id'))

    def get_serializer_class(self):
        if self.action == 'comment':
            return NewsCommentSerializer
        return NewsSerializer

    @action(methods=['POST', 'DELETE'], detail=True)
    def comment(self, request, pk=None):
        news = self.get_object()
        if request.method == 'POST':
            serializer = NewsCommentSerializer(
                data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user, news=news)
            return Response(serializer.data)
        if request.method == 'DELETE':
            comment = get_object_or_404(NewsComment.objects.filter(id=pk))
            if request.user != comment.user:
                return Response({'error': 'ты че дурашечка'}, status=403)
            comment.delete()
            return Response({'message': 'красавчик нефор'})

    @action(methods=['POST'], detail=True, url_path='news')
    def rate_news(self, request, pk=None) -> Response:
        news = self.get_object()
        serializer = RatingSerializer(data=request.data, context={
                                      'request': request, 'news': news})
        serializer.is_valid(raise_exception=True)
        serializer.save(news=news)
        return Response(serializer.data)
