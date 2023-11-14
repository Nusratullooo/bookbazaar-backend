# Generated by Django 3.2.9 on 2023-10-17 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0028_book_hardcover'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='age',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='annotation',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='book',
            name='color',
            field=models.PositiveIntegerField(blank=True, default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='book',
            name='format',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='book',
            name='paper',
            field=models.TextField(blank=True),
        ),
    ]