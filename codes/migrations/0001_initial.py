# Generated by Django 4.2.7 on 2023-11-27 12:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authorization', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConfirmationCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=6, verbose_name='код')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='дата и время создания')),
                ('last_sending_time', models.DateTimeField(verbose_name='дата и время последней отправки')),
                ('confirmation_time', models.DateTimeField(verbose_name='дата и время подтверждения')),
                ('phone_number', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authorization.phonenumber', verbose_name='номер телефона')),
            ],
            options={
                'verbose_name': 'код подтверждения',
                'verbose_name_plural': 'коды подтверждения',
            },
        ),
    ]
