from django.contrib import admin

from .models import University
from .tasks import send_registration_request


class UniverRegistrationAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'approved')
    list_filter = ('approved',)
    actions = ['approve', 'reject']

    def approve(self, request, queryset):
        queryset.update(approved=True)
        recipient_list = [obj.email for obj in queryset]

        send_registration_request.delay(
            recipient_list=recipient_list,
            approved=True
        )

    def reject(self, request, queryset):
        recipient_list = [obj.email for obj in queryset]

        for item in queryset:
            item.delete()

        send_registration_request.delay(
            recipient_list=recipient_list,
            approved=True
        )

    approve.short_description = 'Одобрить'
    reject.short_description = 'Отклонить'


admin.site.register(University, UniverRegistrationAdmin)
