from django.db import models

class OrganizationRegistration(models.Model):
    organization_name = models.CharField(max_length=255)
    organization_address = models.CharField(max_length=255)
    organization_phone_number = models.CharField(max_length=20)
    organization_email = models.EmailField(max_length=255)
    contact_person_name = models.CharField(max_length=255)
    contact_person_phone_number = models.CharField(max_length=20)
    contact_person_email = models.EmailField(max_length=255)
    registration_date = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False) # добавьте это поле

    def __str__(self):
        return self.organization_name

    class Meta:
        verbose_name_plural = "Organization registrations"






