# SPA Приложение, простая реферальная система.
> В данном проекте реализована аутентификация пользователя по номеру телефона, с отправкой одноразового пароля, а так же просмотр и изменение данных профиля пользователя. У каждого пользователя есть персональный инвайт код.
Пользователь может единожды ввести инвайт другого пользователя у себя в ЛК. Реализован как API, так и UI.

>(Так как отправка сообщений это платная функция, имеется лиш функция - заглушка для отправки смс, фактически пароль отправляется на почту и дублируется в ответе от сервера и в интерфейсе пользователя.)

> Проект реализован в целях практики.

### Стек технологий.
- Django + DRF
- PostgreSQL
- Celery
- Simple JWT
- Unittest
- Swagger (drf-yasg)

### Запуск проекта с docker
- Создать в корне проекта файл `.env`
- Заполнить `.env` по шаблону из файла `.env.sample`
- Запустить проект `sudo docker compose up --build`
- По-умолчанию создается суперпользователь логин: `1`, пароль: `1`

### Основные url
- Главная страница: [http://localhost:8000/](http://localhost:8000/)
- doc: [http://localhost:8000/doc/](http://localhost:8000/doc/)
- redoc: [http://localhost:8000/redoc/](http://localhost:8000/redoc/)

### Важно
>Внести в `.env` настройки почтового сервера, а так же указать `RECIPIENT_EMAIL=`, на который будет отправляться пароль для входа, после ввода номера телефона. (Это нужно для имитации отправки смс)

Или:
>Описать функцию отправки смс с кодом на номер телефона:
```Python
# project/users/tasks.py
@shared_task()
def send_otp_to_phone_number(phone: str, otp: str) -> None:
    """Отправить смс с кодом на телефон пользователя.
    Args:
        phone (str): Номер телефона.
        otp (str): Одноразовый пароль.
    """
    pass
```
>в `.env` файле есть два параметра, которые позволяют управлять отправкой кода.
```
SEND_OTP_TO_EMAIL=True 
SEND_OTP_TO_PHONE=False
``` 

### Эндпоинты:
---
POST: [http://127.0.0.1:8000/users/login/](http://127.0.0.1:8000/users/login/)

Тело json:
```
{
    "phone": "+79001003454"
}
``` 
Ответ json:
```
{
    "message": "Код отправлен на телефон(почту) код:$8004"
}
```
---
POST: [http://127.0.0.1:8000/users/verify/](http://127.0.0.1:8000/users/verify/)

Тело json:
```
{
    "phone": "+79001003454",
    "password": "8004"
}
``` 
Ответ json:
```
{
    "access_token": "eyJhbGciOiJ... ...0OuM3VnLuQY",
    "refresh_token": "eyJhbGciOiJ... ...m_Ifb7xG08t0"
}
```
---
POST: [http://127.0.0.1:8000/users/refresh/](http://127.0.0.1:8000/users/refresh/)

Тело json:
```
{
    "refresh_token": "eyJhbGci... ...OiJINjcwYG08t0"
}
``` 
Ответ json:
```
{
    "access_token": "eyJhbGciOiJ... ...iybRSZlqi0Tc"
}
```
---
GET: [http://127.0.0.1:8000/users/retrieve/<телефон_пользователя>/](http://127.0.0.1:8000/users/retrieve/<телефон_пользователя>/)

Ответ json:
```
{
    "id": 1,
    "email": "qwe@qwe.com",
    "phone": "79001003454",
    "first_name": "qwe",
    "last_name": "qwewewe",
    "personal_invitation_code": "enxt0g",
    "someone_invite_code": "efw5fg",
    "invited_users": [
        {
            "phone": "79001003459"
        },
        {
            "phone": "79001003462"
        },
        {
            "phone": "79001003471"
        }
    ]
}
```
---
PATCH \ PUT: [http://127.0.0.1:8000/users/update/<телефон_пользователя>/](http://127.0.0.1:8000/users/update/<телефон_пользователя>/)

Тело json:
```
{
    "email": "qwe@qwe.com",
    "first_name": "Yura",
    "last_name": "Dud'",
    "someone_invite_code": "v7a7re"
}
``` 
Ответ json:
```
{
    "email": "qwe@qwe.com",
    "first_name": "Yura",
    "last_name": "Dud'",
    "someone_invite_code": "v7a7re"
}
```

Покрытие тестами

```
Name                                     Stmts   Miss  Cover
------------------------------------------------------------
config\__init__.py                           2      0   100%
config\asgi.py                               4      4     0%
config\celery.py                             7      0   100%
config\settings.py                          40      0   100%
config\urls.py                               9      0   100%
config\wsgi.py                               4      4     0%
login_ui\__init__.py                         0      0   100%
login_ui\admin.py                            1      0   100%
login_ui\apps.py                             4      0   100%
login_ui\migrations\__init__.py              0      0   100%
login_ui\models.py                           1      0   100%
login_ui\tests.py                            1      0   100%
login_ui\urls.py                             6      0   100%
login_ui\utils\profile_view.py              22     16    27%
login_ui\utils\verify_view.py                3      1    67%
login_ui\views.py                           54     31    43%
manage.py                                   12      2    83%
users\__init__.py                            0      0   100%
users\admin.py                               5      0   100%
users\apps.py                                4      0   100%
users\migrations\0001_initial.py             7      0   100%
users\migrations\__init__.py                 0      0   100%
users\models.py                             15      1    93%
users\permissions.py                         6      0   100%
users\serializers.py                        15      0   100%
users\tasks.py                              14      6    57%
users\tests.py                             105      0   100%
users\urls.py                                5      0   100%
users\utils\doc.py                          10      0   100%
users\utils\login_api_view.py                8      0   100%
users\utils\profile_update_api_view.py      10      2    80%
users\utils\utils.py                        27      0   100%
users\validators.py                         12      0   100%
users\views.py                              89      9    90%
------------------------------------------------------------
TOTAL                                      502     76    85%
```
