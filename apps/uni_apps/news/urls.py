from rest_framework.routers import DefaultRouter
from .views import NewsList, NewsDetail

router = DefaultRouter()
router.register(r'university/(?P<id>\d+)/news', NewsList, 'news')
router.register('news', NewsDetail, 'news')

urlpatterns = router.urls
