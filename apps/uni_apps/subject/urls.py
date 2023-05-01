from rest_framework.routers import DefaultRouter

from .views import SubjectList, SubjectDetail, SkillReadCreateDeleteView

router = DefaultRouter()
router.register(r'university/(?P<id>\d+)/subject', SubjectList, 'subject')
router.register('subject', SubjectDetail, 'subject')
router.register('skill', SkillReadCreateDeleteView, 'skill')

urlpatterns = router.urls
