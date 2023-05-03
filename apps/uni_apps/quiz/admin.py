from django.contrib import admin

from .models import Quiz, Question, Answer


class AnswerInline(admin.TabularInline):
    model = Answer


class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]
    list_display = ('text', 'quiz')
    list_filter = ['quiz']

class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject')


admin.site.register(Question, QuestionAdmin)
admin.site.register(Quiz, QuizAdmin)
