# Generated by Django 3.2.9 on 2022-10-19 00:35

from django.db import migrations, models
import main.apps.account.utils


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0024_user_user_generate_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='expiration_time_register',
            field=models.CharField(blank=True, default=main.apps.account.utils.user_expire_time, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='expiration_time_reset',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
