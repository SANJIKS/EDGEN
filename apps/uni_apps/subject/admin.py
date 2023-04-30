from django.contrib import admin

from .models import Subject, Skill


admin.site.register([Subject, Skill])
