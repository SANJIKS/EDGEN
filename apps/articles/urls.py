from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import ArticleViewSet, FavoriteListAPIView, RecommendationsListAPIView, TagsCreateReadDeleteView

router = DefaultRouter()
router.register('article', ArticleViewSet, 'articles')
router.register('tag', TagsCreateReadDeleteView, 'tags')

urlpatterns = [
    path('', include(router.urls)),
    path('article/favorites/', FavoriteListAPIView.as_view(), name='favorites'),
    path('article/recommendations/', RecommendationsListAPIView.as_view(), name='top-articles')
]
