from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import UniversityViewSet

router = DefaultRouter()
router.register('university', UniversityViewSet, 'university')

urlpatterns = router.urls
