from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CustomUserViewSet, ProfileViewSet, SubscriptionViewSet, SubscriptionListView

router = DefaultRouter()
router.register('user', CustomUserViewSet, 'user')

urlpatterns = [
    path('', include('djoser.urls.jwt')),
    path('', include(router.urls)),
    path('user/<int:id>/profile/', ProfileViewSet.as_view({
        'get': 'retrieve', })),
    path('user/me/profile/', ProfileViewSet.as_view({
        'put': 'me',
        'patch': 'me', })),
    path('user/<int:id>/subscribe/', SubscriptionViewSet.as_view({'post': 'create'}),
         name='subscription-create'),
    path('user/<int:id>/unsubscribe/', SubscriptionViewSet.as_view({'delete': 'destroy'}),
         name='subscription-delete'),
    path('user/me/subscriptions/', SubscriptionListView.as_view(),
         name='subscription-list'),
]
