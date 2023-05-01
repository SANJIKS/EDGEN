from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CustomUserViewSet, ProfileViewSet , SubscriptionCreateAPIView , SubscriptionDestroyAPIView , SubscriptionListAPIView 

router = DefaultRouter()
router.register('user', CustomUserViewSet, 'user')

urlpatterns = [
    path('', include('djoser.urls.jwt')),
    path('', include(router.urls)),
    path('user/<int:id>/profile/', ProfileViewSet.as_view({
        'get': 'retrieve',})),
    path('user/me/profile/', ProfileViewSet.as_view({
        'put': 'me',
        'patch': 'me',})),
    path('auth/user/<int:user_id>/subscribe/', SubscriptionCreateAPIView.as_view(), name='subscription-create'),
    path('auth/user/<int:user_id>/subscriptions/', SubscriptionListAPIView.as_view(), name='subscription-list'),
    path('auth/user/<int:user_id>/subscriptions/delete/', SubscriptionDestroyAPIView.as_view(), name='subscription-delete'),

]
