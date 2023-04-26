from django.contrib import admin
from .models import OrganizationRegistration

class OrganizationRegistrationAdmin(admin.ModelAdmin):
    list_display = ('organization_name', 'registration_date')
    list_filter = ('registration_date', )
    actions = ['approve_selected_organizations']

    def approve_selected_organizations(self, request, queryset):
        queryset.update(approved=True)

    approve_selected_organizations.short_description = "Approve selected organizations"

admin.site.register(OrganizationRegistration, OrganizationRegistrationAdmin)
