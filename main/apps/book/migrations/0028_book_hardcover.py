# Generated by Django 3.2.9 on 2022-10-29 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0027_remove_book_hardcover'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='hardcover',
            field=models.BooleanField(default=False),
        ),
    ]
