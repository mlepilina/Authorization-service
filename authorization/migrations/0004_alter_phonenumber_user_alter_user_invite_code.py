# Generated by Django 4.2.7 on 2023-12-01 04:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authorization', '0003_alter_phonenumber_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phonenumber',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='phone', to=settings.AUTH_USER_MODEL, verbose_name='пользователь'),
        ),
        migrations.AlterField(
            model_name='user',
            name='invite_code',
            field=models.CharField(max_length=6, unique=True, verbose_name='инвайт-код'),
        ),
    ]