from rest_framework.routers import DefaultRouter
from .views import LectureViewSet

router = DefaultRouter()
router.register(r'university/(?P<uni_id>\d+)/subject/(?P<sub_id>\d+)/lecture',
                LectureViewSet, 'lecture')

urlpatterns = router.urls
