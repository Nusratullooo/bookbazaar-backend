# Generated by Django 3.2.9 on 2023-10-23 08:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0036_alter_book_cover_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='hardcover',
        ),
    ]