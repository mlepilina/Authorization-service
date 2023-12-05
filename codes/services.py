from django.db.models import ObjectDoesNotExist
from django.utils.crypto import get_random_string
from django.utils import timezone

from codes.models import ConfirmationCode
from authorization.models import PhoneNumber
from codes.tasks import send_message


def can_send_code(phone_number: PhoneNumber) -> bool:
    """
    Проверяет, можно ли отправить на данный номер код подтверждения.
    Код можно отправить, если такой номер телефона существует в базе
    и если за последнюю минуту код не отправлялся.
    """
    try:
        code = ConfirmationCode.objects.get(
            phone_number=phone_number,
            confirmation_time__isnull=True,
            last_sending_time__isnull=False
        )
    except ObjectDoesNotExist:
        return True

    if code.last_sending_time > (timezone.now() - timezone.timedelta(minutes=1)):
        return False

    return True


def is_wasted_code(code: ConfirmationCode):
    """
    Проверят, не был ли код просрочен.
    Если код старше 10 минут, то, значит, он просрочен - возвращается True.
    Иначе False
    """

    if code.create_date < (timezone.now() - timezone.timedelta(minutes=10)):
        return True

    return False


def generate_new_code(phone_number: PhoneNumber) -> ConfirmationCode:
    """Рандомно генерирует строку для кода подтверждения и создаёт обьект кода."""

    new_code = get_random_string(length=ConfirmationCode.CODE_LENGTH, allowed_chars="0123456789")
    code = ConfirmationCode.objects.create(
        code=new_code,
        phone_number=phone_number,
    )

    return code


def get_or_create_code(phone_number: PhoneNumber) -> ConfirmationCode:
    """
    Получает или создаёт объект модели кода подтверждения ConfirmationCode по номеру телефона.
    Проверят, не был ли код просрочен.
    Возвращает актуальный код подтверждения.
    """

    try:
        current_code = ConfirmationCode.objects.get(
            phone_number=phone_number,
            confirmation_time__isnull=True,
            create_date__gte=(timezone.now() - timezone.timedelta(minutes=10))
        )
    except ObjectDoesNotExist:
        return generate_new_code(phone_number)

    if is_wasted_code(current_code):
        return generate_new_code(phone_number)

    return current_code


def send_code(code: ConfirmationCode) -> None:
    """Отправляет код подтверждения на номер телефона."""
    send_message.delay(code.pk)


def is_valid_code(code: str, phone_number: str) -> bool:
    """
    Проверяет, валидный ли код по данному номеру телефона:

    1) Код не должен быть уже проверенным ранее.
    2) Код должен существовать в базе, привязанным к данному номеру телефона.

    После успешной проверки устанавливает объекту модели кода ConfirmationCode
    поле confirmation_time в текущий момент
    """

    try:
        phone_number = PhoneNumber.objects.get(phone_number=phone_number)
        code_object = ConfirmationCode.objects.get(
            code=code,
            phone_number=phone_number,
            confirmation_time__isnull=True,
            create_date__gte=(timezone.now() - timezone.timedelta(minutes=10))
        )
    except ObjectDoesNotExist:
        return False

    code_object.confirmation_time = timezone.now()
    code_object.save()

    return True
