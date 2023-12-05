from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):

    email = None
    username = None
    password = None
    first_name = None
    last_name = None

    INVITE_CODE_LENGTH = 6

    surname = models.CharField(max_length=100, verbose_name='фамилия', **NULLABLE)
    name = models.CharField(max_length=100, verbose_name='имя', **NULLABLE)
    patronymic = models.CharField(max_length=100, verbose_name='отчество', **NULLABLE)
    invite_code = models.CharField(max_length=INVITE_CODE_LENGTH, verbose_name='инвайт-код', unique=True)
    friend_invite_code = models.CharField(max_length=INVITE_CODE_LENGTH, verbose_name='инвайт-код от друга', **NULLABLE)
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')

    USERNAME_FIELD = "id"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'User id:{self.id} phone:{self.phone and self.phone.phone_number}'


class PhoneNumber(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='пользователь', related_name='phone', **NULLABLE)
    phone_number = models.CharField(max_length=40, verbose_name='номер')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')

    class Meta:
        verbose_name = 'номер телефона'
        verbose_name_plural = 'номера телефонов'

    def __str__(self):
        return f'{self.number}{self.user}{self.create_date}'
