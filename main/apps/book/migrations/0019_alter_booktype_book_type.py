# Generated by Django 3.2.9 on 2022-08-30 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0018_alter_booktype_book_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booktype',
            name='book_type',
            field=models.CharField(choices=[('online', 'online'), ('paper', 'paper'), ('audio', 'audio')], default='paper', max_length=10),
        ),
    ]
