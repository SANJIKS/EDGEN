from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import CustomUserViewSet

router = DefaultRouter()
router.register('user', CustomUserViewSet, 'user')

urlpatterns = router.urls
