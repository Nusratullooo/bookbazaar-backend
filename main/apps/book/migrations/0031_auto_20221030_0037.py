# Generated by Django 3.2.9 on 2022-10-29 19:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0030_auto_20221030_0023'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='hard_cover',
        ),
        migrations.RemoveField(
            model_name='book',
            name='hard_cover_en',
        ),
        migrations.RemoveField(
            model_name='book',
            name='hard_cover_ru',
        ),
        migrations.RemoveField(
            model_name='book',
            name='hard_cover_uz',
        ),
    ]
