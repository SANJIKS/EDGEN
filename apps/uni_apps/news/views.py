from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, status, viewsets, generics
from rest_framework.decorators import action
from rest_framework.response import Response

from ..permissions import IsOwner
from ..university.models import University
from .models import News, NewsComment
from .serializers import (NewsCommentSerializer, NewsSerializer,
                          RatingSerializer)


class NewsList(mixins.ListModelMixin,
               mixins.CreateModelMixin,
               viewsets.GenericViewSet):
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['title', 'description']
    serializer_class = NewsSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsOwner()]
        return [permissions.AllowAny()]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if getattr(self, 'swagger_fake_view', False):
            return context

        university = get_object_or_404(
            University, id=self.kwargs.get('id'))
        context.update({
            'request': self.request,
            'university': university
        })
        return context

    def get_queryset(self):
        return News.objects.filter(university=self.kwargs.get('id'))
    
class AllNewsView(generics.ListAPIView):
    serializer_class = NewsSerializer

    def get_queryset(self):
        return News.objects.all()


class NewsDetail(mixins.RetrieveModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin,
                 viewsets.GenericViewSet):
    queryset = News.objects.all()

    def get_permissions(self):
        if self.action in ('comment', 'rate'):
            return [permissions.IsAuthenticated()]
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsOwner()]
        return [permissions.AllowAny()]

    def get_serializer_class(self):
        if self.action == 'comment_create':
            return NewsCommentSerializer
        elif self.action == 'rate':
            return RatingSerializer
        return NewsSerializer

    @action(methods=['POST'], detail=True, url_path='comment')
    def comment_create(self, request, pk=None):
        news = self.get_object()
        serializer = self.get_serializer(
            data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, news=news)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(['DELETE'], detail=True, url_path='comment/(?P<comment_pk>\d+)')
    def comment_delete(self, request, pk=None, comment_pk=None):
        comment = get_object_or_404(NewsComment.objects.filter(pk=comment_pk))
        if request.user != comment.user:
            return Response({'detail': 'You are not allowed to perform this action'}, status=status.HTTP_403_FORBIDDEN)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['POST'], detail=True)
    def rate(self, request, pk=None) -> Response:
        news = self.get_object()
        serializer = RatingSerializer(data=request.data, context={
                                      'request': request, 'news': news})
        serializer.is_valid(raise_exception=True)
        serializer.save(news=news)
        return Response(serializer.data)
