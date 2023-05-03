from rest_framework.routers import DefaultRouter
from .views import NewsList, NewsDetail, AllNewsView
from django.urls import path, include

router = DefaultRouter()
router.register(r'university/(?P<id>\d+)/news', NewsList, 'news')
router.register('news', NewsDetail, 'news')

urlpatterns = [
    path('', include(router.urls)),
    path('news/', AllNewsView.as_view(), name='allnews')
]
