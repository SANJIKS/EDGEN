from django.contrib import admin

from .models import Lecture, LectureFile


class LectureFileInline(admin.TabularInline):
    model = LectureFile


class LectureAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at', 'user']
    inlines = [LectureFileInline]


admin.site.register(Lecture, LectureAdmin)
