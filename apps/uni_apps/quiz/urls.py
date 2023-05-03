from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter

from .views import QuizDetail, QuizList, QuestionList, QuestionDetail


router = DefaultRouter()
router.register(r'subject/(?P<id>\d+)/quiz', QuizList, 'quiz')
router.register('quiz', QuizDetail, 'quiz')
router.register(r'quiz/(?P<id>\d+)/question', QuestionList, 'question')
router.register('question', QuestionDetail, 'question')

urlpatterns = router.urls
