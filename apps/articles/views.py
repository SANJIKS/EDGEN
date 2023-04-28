from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, mixins, permissions, viewsets



from .models import Article, Comment, Like, DisLike, Favorite, Tags
from .serializers import ArticleSerializer, FavoriteSerializer, LikeSerializer, DisLikeSerializer, CommentSerializer, TagsSerializer
from .permissions import IsAuthor


class ArticleViewSet(ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['title', 'description']


    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [IsAuthenticated]
        elif self.request.method in ['PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [IsAuthor]
        return super().get_permissions()


    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context
    
    def get_serializer_class(self):
        if self.action == 'comment':
            return CommentSerializer
        elif self.action == 'like':
            return LikeSerializer
        elif self.action == 'dislike':
            return DisLikeSerializer
        elif self.action == 'favorite':
            return FavoriteSerializer
        return super().get_serializer_class()

    @action(methods=['POST', 'DELETE'], detail=True)
    def comment(self, request, pk=None):
        article = self.get_object()
        if request.method == 'POST':
            serializer = CommentSerializer(data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user, article=article)
            return Response(serializer.data)
        if request.method == 'DELETE':
            comment = get_object_or_404(Comment.objects.filter(id=pk))
            if request.user != comment.user:
                return Response({'error': 'ты че дурашечка'}, status=403)
            comment.delete()
            return Response({'message': 'красавчик нефор'})
        

    @action(methods=['POST'], detail=True)
    def like(self, request, pk=None):
        article = self.get_object()
        like = Like.objects.filter(user=request.user, article=article)
        if like.exists():
            like.delete()
            liked = False
            article.rating -= 1
        else:
            Like.objects.create(user=request.user, article=article)
            liked = True
            article.rating += 1
            dislike = DisLike.objects.filter(user=request.user, article=article)
            if dislike.exists():
                dislike.delete()
                article.rating += 1

        likes_count = Like.objects.filter(article=article).count()
        response_data = {'liked': liked, 'likes_count': likes_count}
        return Response(response_data)
    
    @action(methods=['POST'], detail=True)
    def dislike(self, request, pk=None):
        article = self.get_object()
        dislike = DisLike.objects.filter(user=request.user, article=article)
        if dislike.exists():
            dislike.delete()
            disliked = False
            article.rating += 1
        else:
            DisLike.objects.create(user=request.user, article=article)
            disliked = True
            article.rating -= 1
            like = Like.objects.filter(user=request.user, article=article)
            if like.exists():
                like.delete()
                article.rating -= 1
        return Response({'DisLiked': disliked})
    
    
    @action(methods=['POST'], detail=True)
    def favorite(self, request, pk=None):
        article = self.get_object()
        favor = Favorite.objects.filter(user=request.user, article=article)
        if favor.exists():
            favor.delete()
            favor = False
        else:
            Favorite.objects.create(user=request.user, article=article)
            favor = True

        return Response({'In Favorite': favor})
    

class FavoriteListAPIView(generics.ListAPIView):
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Favorite.objects.filter(user=user)


class RecommendationsListAPIView(generics.ListAPIView):
    serializer_class = ArticleSerializer

    def get_queryset(self):
        return Article.objects.order_by('-rating')[:10]

class TagsCreateReadDeleteView(mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer

    def get_permissions(self):
        method = self.request.method
        if method in permissions.SAFE_METHODS:
            self.permission_classes = [permissions.AllowAny]
        elif method in ['POST', 'DELETE']:
            self.permission_classes = [permissions.IsAdminUser]
        return super().get_permissions()
    


# class CommentViewSet(ModelViewSet):
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer

#     def get_permissions(self):
#         if self.action == 'create':
#             self.permission_classes = [IsAuthenticated]
#         elif self.action in ['update', 'destroy']:
#             self.permission_classes = [IsAuthor]
#         return super().get_permissions()
    
#     def get_serializer_context(self):
#         context = super().get_serializer_context()
#         context.update({'request': self.request})
#         return context