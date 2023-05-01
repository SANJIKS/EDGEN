from rest_framework.routers import DefaultRouter
from .views import LectureList, LectureDetail

router = DefaultRouter()
router.register(r'subject/(?P<id>\d+)/lecture',
                LectureList, 'lecture')
router.register('lecture', LectureDetail, 'lecture')

urlpatterns = router.urls
