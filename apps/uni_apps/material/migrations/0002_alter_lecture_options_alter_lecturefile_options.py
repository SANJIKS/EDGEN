# Generated by Django 4.2 on 2023-05-01 10:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('material', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lecture',
            options={'verbose_name': 'Лекция', 'verbose_name_plural': 'Лекции'},
        ),
        migrations.AlterModelOptions(
            name='lecturefile',
            options={'verbose_name': 'Файл лекции', 'verbose_name_plural': 'Файлы лекции'},
        ),
    ]
