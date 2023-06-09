# Generated by Django 4.2 on 2023-04-28 13:00

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('university', '0003_university_students'),
    ]

    operations = [
        migrations.AlterField(
            model_name='university',
            name='students',
            field=models.ManyToManyField(blank=True, related_name='courses', to=settings.AUTH_USER_MODEL),
        ),
    ]
