# Generated by Django 4.2 on 2023-04-27 14:38

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('university', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='university',
            name='owners',
            field=models.ManyToManyField(related_name='universities', to=settings.AUTH_USER_MODEL),
        ),
    ]
