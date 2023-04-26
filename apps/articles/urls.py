from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import ArticleViewSet, FavoriteListAPIView, RecommendationsListAPIView

router = DefaultRouter()
router.register('article', ArticleViewSet, 'articles')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/favorites/', FavoriteListAPIView.as_view(), name='favorites'),
    path('auth/recommendations/', RecommendationsListAPIView.as_view(), name='top-articles')
]