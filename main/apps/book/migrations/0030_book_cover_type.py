# Generated by Django 3.2.9 on 2023-10-18 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0029_auto_20231017_1653'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='cover_type',
            field=models.CharField(choices=[('SewnWithWire1', 'Sewnwithwire1'), ('SewnWithWire2', 'Sewnwithwire2'), ('SewnWithWire3', 'Sewnwithwire3')], default='SewnWithWire1', max_length=100),
        ),
    ]
