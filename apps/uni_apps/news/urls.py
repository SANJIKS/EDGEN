from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import NewsViewSet

router = DefaultRouter()
router.register(r'university/(?P<uni_id>\d+)/news', NewsViewSet, 'news')

urlpatterns = router.urls
