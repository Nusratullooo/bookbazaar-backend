# Generated by Django 3.2.9 on 2023-10-18 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0032_auto_20231018_1236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='cover_type',
            field=models.CharField(choices=[('Wire cover', 'Type 1'), ('Soft cover', 'Type 2'), ('Hard cover', 'Type 3')], default='Wire cover', max_length=100),
        ),
    ]
