from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from authorization import services
from codes.services import can_send_code, get_or_create_code, is_valid_code
from codes.services import send_code


class UserServiceView(APIView):

    permission_classes = (AllowAny,)
    authentication_classes = []

    def post(self, request: Request) -> Response:
        """
        Авторизация шаг 1.
        Пользователь вводит номер телефона,
        происходит проверка его корректности,
        отправлется код
        """

        raw_number = str(request.data.get("phone_number", ''))
        if not raw_number:
            return Response(data={'error': 'Отсутсвуют поля phone_number'}, status=status.HTTP_400_BAD_REQUEST)
        elif not services.validate_phone_string(raw_number):
            return Response(data={'error': 'Некорректный номер телефона'}, status=status.HTTP_400_BAD_REQUEST)

        phone_number = services.get_or_create_phone(raw_number)
        if not can_send_code(phone_number):
            return Response(
                data={'error': 'Код можно отпралять только 1 раз в минуту'}, status=status.HTTP_400_BAD_REQUEST
            )

        confirmation_code = get_or_create_code(phone_number)
        send_code(confirmation_code)
        return Response(status=status.HTTP_200_OK)

    def put(self, request: Request) -> Response:
        """
        Авторизация шаг 2.
        Пользователь вводит полученный код,
        происходит проверка корректности кода,
        происходит авторизация пользователя с получением jwt-токенов.
        """

        raw_number = str(request.data.get('phone_number', None))
        code = str(request.data.get('code', None))

        if not (raw_number or code):
            return Response(data={'error': 'Отсутсвуют поля phone_number и code'}, status=status.HTTP_400_BAD_REQUEST)
        elif not is_valid_code(code, raw_number):
            return Response(data={'error': 'Данный код недействителен'}, status=status.HTTP_400_BAD_REQUEST)

        new_user = services.get_or_create_user(raw_number)
        tokens = services.create_jwt_token(new_user)
        return Response(data=tokens, status=status.HTTP_200_OK)


class UserInfoView(APIView):

    def get(self, request: Request) -> Response:
        """Запрос на профиль пользователя"""
        return Response(data=services.get_profile_info(request.user))


class UserInviteView(APIView):

    def get(self, request: Request) -> Response:
        """Запрос на список пользователей, которые ввели инвайт код текущего пользователя."""
        invited_users = services.get_invited_users(request.user)
        result = [services.get_profile_info(user) for user in invited_users]
        return Response(data=result)

    def post(self, request: Request) -> Response:
        """Установка чужого инвайт-кода."""

        invite_code = request.data.get('invite_code', None)
        if invite_code is None:
            return Response(data={'error': 'Отсутствует invite_code'}, status=status.HTTP_400_BAD_REQUEST)
        elif not services.invite_code_exist(invite_code):
            return Response(data={'error': 'Такого кода не существует'}, status=status.HTTP_400_BAD_REQUEST)
        elif services.check_correct_invite_code(invite_code=invite_code, user=request.user):
            return Response(data={'error': 'Пользователь с этим кодом зарегистрирован позже вас'}, status=status.HTTP_400_BAD_REQUEST)
        elif request.user.friend_invite_code:
            return Response(data={'error': 'Инвайт-код уже установлен'}, status=status.HTTP_400_BAD_REQUEST)

        services.set_friend_invite_code(user=request.user, invite_code=invite_code)

        return Response()
