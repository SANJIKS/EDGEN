from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CustomUserViewSet, ProfileViewSet

router = DefaultRouter()
router.register('user', CustomUserViewSet, 'user')

urlpatterns = [
    path('', include('djoser.urls.jwt')),
    path('', include(router.urls)),
    path('user/<int:id>/profile/', ProfileViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update'})),
]
