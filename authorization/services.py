from django.db.models import ObjectDoesNotExist, QuerySet
from django.utils.crypto import get_random_string
from rest_framework_simplejwt.tokens import RefreshToken

from authorization.models import PhoneNumber, User


def get_or_create_phone(number: str) -> PhoneNumber:
    """Получает или создаёт объект модели PhoneNumber по номеру телефона."""

    try:
        phone_number = PhoneNumber.objects.get(phone_number=number)
    except ObjectDoesNotExist:
        phone_number = PhoneNumber.objects.create(phone_number=number)

    return phone_number


def get_or_create_user(number: str) -> User:
    """Получает или создаёт пользователя (объект модели User) по номеру телефона."""

    phone_number = get_or_create_phone(number)

    if phone_number.user:
        return phone_number.user

    user = User.objects.create(
        invite_code=generate_invite_code()
    )

    phone_number.user = user
    phone_number.save()

    return user


def generate_invite_code() -> str:
    """Создаёт рандомный уникальный инвайт-код из символов и цифр."""

    while True:
        new_code = get_random_string(
            length=User.INVITE_CODE_LENGTH,
            allowed_chars="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        )
        try:
            User.objects.get(invite_code=new_code)
        except ObjectDoesNotExist:
            return new_code


def check_correct_invite_code(invite_code: str, user: User):
    """
    Проверяет корректность введенного инвайт-кода:
    возвращает True, если данный код есть в базе и
    если владелец данного кода (User) был зарегистрирован раньше,
    чем пользователь, который ввёл данный код.
    """
    try:
        user_with_code = User.objects.get(invite_code=invite_code)
    except ObjectDoesNotExist:
        return False

    if user.create_date < user_with_code.create_date:
        return False

    return True


def invite_code_exist(invite_code: str) -> bool:
    """Проверяет, существует ли владелец (пользователь) введённого инвайт-кода."""

    try:
        User.objects.get(invite_code=invite_code)
    except ObjectDoesNotExist:
        return False
    else:
        return True


def set_friend_invite_code(user: User, invite_code: str):
    """Устанавливает текущему пользователю введённый инвайт-код от друга."""

    user.friend_invite_code = invite_code
    user.save()


def validate_phone_string(number: str) -> bool:
    """Проверяет, соответствует ли строка паттерну номера телефона."""

    if number.startswith('+'):
        number = number[1:]

    return number.isdigit() and len(number) > 10


def create_jwt_token(user: User):
    """Создаёт refresh- и access- токены."""

    refresh_token = RefreshToken.for_user(user)

    data = {
        'refresh': str(refresh_token),
        'access': str(refresh_token.access_token)
    }
    return data


def get_profile_info(user: User):
    """Возвращает информацию о профиле пользователя."""

    info = {
        'id': user.pk,
        'name': user.name,
        'surname': user.surname,
        'patronymic': user.patronymic,
        'invite_code': user.invite_code,
        'friend_invite_code': user.friend_invite_code,
        'phone': user.phone.phone_number,
    }

    return info


def get_invited_users(user: User) -> QuerySet[User]:
    """Возвращает всех пользователей, которые приглашены данным пользователем."""
    return User.objects.filter(friend_invite_code=user.invite_code)
