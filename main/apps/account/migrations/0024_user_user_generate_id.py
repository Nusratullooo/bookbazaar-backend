# Generated by Django 3.2.9 on 2022-10-14 05:16

from django.db import migrations, models
import main.apps.account.utils


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0023_auto_20220823_0932'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_generate_id',
            field=models.CharField(default=main.apps.account.utils.generate_random_password_user, max_length=6),
        ),
    ]
