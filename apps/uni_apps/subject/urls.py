from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import SubjectViewSet

router = DefaultRouter()
router.register(r'university/(?P<uni_id>\d+)/subject',
                SubjectViewSet, 'university_subject')

urlpatterns = router.urls
