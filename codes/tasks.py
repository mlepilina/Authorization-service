import time

from django.utils import timezone

from codes.models import ConfirmationCode
from config.celery import app


@app.task
def send_message(code_id: int):
    """
    Отправляет код подтверждения
    """
    time.sleep(2)
    code = ConfirmationCode.objects.get(pk=code_id)
    code.last_sending_time = timezone.now()
    code.save()
    print(f'Отправлен код {code.code} на номер {code.phone_number.phone_number}')