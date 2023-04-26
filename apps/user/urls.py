from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CustomUserViewSet, ProfileViewSet

router = DefaultRouter()
router.register('user', CustomUserViewSet, 'user')
router.register('user/<id>/profile', ProfileViewSet, 'profile')

urlpatterns = [
    path('', include('djoser.urls.jwt')),
    path('', include(router.urls)),
]
