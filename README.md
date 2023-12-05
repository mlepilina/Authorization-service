# Authorization-service



## Запуск в Docker

Создайте файл .env на основе примера .env.example, заполните его корректными значениями. 

Для запуска наберите команду:

```shell
docker-compose up --build
```

## API документация

### Авторизация

---
#### Шаг 1. Отправка номера телефона 

`POST: https://<domain>/authorization/`

`Content-Type: application/json`

Обязательные параметры:

`phone_number` - ваш номер телефона. Длина больше 10 символов.

Пример:

```json
{
    "phone_number": "89999999990"
}
```
Результат:
На переданный номер телефона будет отправлен секретный код из 6 цифр.

`Respose 200 OK`

---

#### Шаг 2. Отправка кода подтверждения

`PUT: https://<domain>/authorization/`

`Content-Type: application/json`

Обязательные параметры:

`phone_number` - ваш номер телефона, отправленный ранее на шаге 1.

`code` - Секретный код, который отправляется сервером на номер телефона.

Пример:

```json
{
    "phone_number": "89999999990",
    "code": "123456"
}
```

Результат:
Пользователь авторизуется в системе.

`Respose 200 OK`
```json
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcwMTY4ODc4MSwiaWF0IjoxNzAxNjAyMzgxLCJqdGkiOiIwODk0ZDAyMzczMzY0ZTVkYTM1ODQwOTk3NTU1MzRlMyIsInVzZXJfaWQiOjExfQ.PAg_QRVWZTzHUYTho7nDYKDM1MH5aFogSU1nPbfoyA8",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAxNjIzOTgxLCJpYXQiOjE3MDE2MDIzODEsImp0aSI6IjdlM2NiNzgwNzM4YTRmNmFhNTMzNzY0YjYwZjhkYTMyIiwidXNlcl9pZCI6MTF9.bW8jBo3tuRVD_C6vj-BsMZdSDV-2nbnAEIbV6YDzNeA"
}
```

---


### Запрос на профиль пользователя

`GET: https://<domain>/info/`

`Authorization: Bearer Token`

Результат:

```json
{
    "id": 1,
    "name": null,
    "surname": null,
    "patronymic": null,
    "invite_code": "17PPai",
    "friend_invite_code": null,
    "phone": "89090099900"
}
```

Вывод личной информации текущего пользователя.

`Respose 200 OK`

---


### Получение информации о приглашенных пользователях

`GET: https://<domain>/info/invite/`

`Authorization: Bearer Token`

Результат:

```json
[
    {
        "id": 10,
        "name": "Maria",
        "surname": null,
        "patronymic": null,
        "invite_code": "18Phji",
        "friend_invite_code": "17PPai",
        "phone": "89090066678"
    },
    {
        "id": 8,
        "name": null,
        "surname": null,
        "patronymic": null,
        "invite_code": "89KGpwl",
        "friend_invite_code": "17PPai",
        "phone": "89090066670"
    }
]
```

Вывод личной информации пользователей, которые ввели инвайт-код текущего пользователя.

`Respose 200 OK`

---


### Установка чужого инвайт-кода

`POST: https://<domain>/info/invite/`

`Content-Type: application/json`
`Authorization: Bearer Token`

Обязательные параметры:

`invite_code` - чужой инвайт-код (друга)

Пример:

```json
{
    "invite_code": "17PPai"
}
```

Результат:
При корректном вводе чужой инвайт код устанавливается в личных данных текущего пользователя (поле `friend_invite_code`). У владельца инвайт-кода появляется возможность посмотреть данные пользователя, который ввёл код.

`Respose 200 OK`


---


### Обновление токена

`POST: https://<domain>/info/refresh/`

`Content-Type: application/json`

Обязательные параметры:

`refresh` - refresh-token

Пример:

```json
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcwMTg0NjcwMywiaWF0IjoxNzAxNzYwMzAzLCJqdGkiOiIyNTc4MDI5YjY4Y2E0Y2UxYjA1NzY4YzhiNTFiYjA5OCIsInVzZXJfaWQiOjF9.iWwaNa8P9hkOTtZZirPvZUR1YWCt5sIr0C0jrPSlmPU"
}
```

Результат:
Получение нового access-токена.

```json
{
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAxNzgyMTIzLCJpYXQiOjE3MDE3NjAzMDMsImp0aSI6ImI2MmMxNjE2MGFhYjQ5Y2U4ZDdjMTFjNmYzMTViMDc3IiwidXNlcl9pZCI6MX0.eMKLJVvght8OlEyu0lLbkBCFwzkF5Jlmr-r5PT1BK24"
}
```

`Respose 200 OK`


---

### Выход из системы

`POST: https://<domain>/info/logout/`

`Content-Type: application/json`

Обязательные параметры:

`refresh` - refresh-token

Пример:

```json
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcwMTg0NjcwMywiaWF0IjoxNzAxNzYwMzAzLCJqdGkiOiIyNTc4MDI5YjY4Y2E0Y2UxYjA1NzY4YzhiNTFiYjA5OCIsInVzZXJfaWQiOjF9.iWwaNa8P9hkOTtZZirPvZUR1YWCt5sIr0C0jrPSlmPU"
}
```

Результат:
Занесение токена в черный список.

`Respose 200 OK`


---

