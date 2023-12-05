from django.db import models

from authorization.models import PhoneNumber

NULLABLE = {'blank': True, 'null': True}


class ConfirmationCode(models.Model):
    CODE_LENGTH = 6

    phone_number = models.ForeignKey(PhoneNumber, on_delete=models.CASCADE, verbose_name='номер телефона')
    code = models.CharField(max_length=CODE_LENGTH, verbose_name='код')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='дата и время создания')
    last_sending_time = models.DateTimeField(verbose_name='дата и время последней отправки', **NULLABLE)
    confirmation_time = models.DateTimeField(verbose_name='дата и время подтверждения', **NULLABLE)

    class Meta:
        verbose_name = 'код подтверждения'
        verbose_name_plural = 'коды подтверждения'

    def __str__(self):
        return f'{self.code}{self.phone_number}'
