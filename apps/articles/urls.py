from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (ArticleViewSet, FavoriteListAPIView,
                    RecommendationsListAPIView, TagsCreateReadDeleteView)

router = DefaultRouter()
router.register('article', ArticleViewSet, 'articles')
router.register('tag', TagsCreateReadDeleteView, 'tags')

urlpatterns = [
    path('', include(router.urls)),
    path('article/favorites/', FavoriteListAPIView.as_view(), name='favorites'),
    path('recommendations/', RecommendationsListAPIView.as_view())
]
