# Generated by Django 4.2 on 2023-04-25 23:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OrganizationRegistration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('organization_name', models.CharField(max_length=255)),
                ('organization_address', models.CharField(max_length=255)),
                ('organization_phone_number', models.CharField(max_length=20)),
                ('organization_email', models.EmailField(max_length=255)),
                ('contact_person_name', models.CharField(max_length=255)),
                ('contact_person_phone_number', models.CharField(max_length=20)),
                ('contact_person_email', models.EmailField(max_length=255)),
                ('registration_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Organization registrations',
            },
        ),
    ]
