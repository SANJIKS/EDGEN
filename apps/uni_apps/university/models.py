from django.db import models


class University(models.Model):
    owners = models.ManyToManyField('auth.User', related_name='universities')
    students = models.ManyToManyField(
        'auth.User', related_name='courses', blank=True)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    email = models.EmailField()
    approved = models.BooleanField(default=False)
    description = models.TextField()
    avatar = models.ImageField(upload_to='universities', default='universities/default.jpg')
    registration_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Универ"
        verbose_name_plural = "Универы"

    def __str__(self):
        return self.name

