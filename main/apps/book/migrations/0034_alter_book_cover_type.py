# Generated by Django 3.2.9 on 2023-10-18 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0033_alter_book_cover_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='cover_type',
            field=models.CharField(choices=[('Wire cover', 'Wire Cover'), ('Soft cover', 'Soft Cover'), ('Hard cover', 'Hard Cover')], default='Wire cover', max_length=100),
        ),
    ]
