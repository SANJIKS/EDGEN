from django.contrib import admin

from .models import Profile, Subscription

admin.site.register([Profile, Subscription])

