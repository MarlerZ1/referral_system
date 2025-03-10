# Введение
В данном документе будет описан способ запуска приложения для тестового задания.


Приложение развернуто на сайте, для доступа:
- Админка:  http://94.250.252.8/admin
- Swagger:  http://94.250.252.8/docs/swagger
- ReDoc:  http://94.250.252.8/docs/redoc

Аккаунт администратора:
- Логин: admin
- Пароль: template_password_098

Тестовое задание представляет собой rest api проект для реферальной системы. Для авторизации используется Oauth 2.0, для документации - swagger / redoc. Указываемый при регистрации email проверяется с помощью сервиса emailhunter.co. I/O Bound задачи асинхронны насколько позволяет фреймворк. Реферальные коды кешируются в redis базу данных. Проект обернут в Docker + nginx.

# Запуск приложения
## Последовательность действий
Для локального развертывания необходимо
- скачать проект;
- у файлf .env.template убрать .template;
- заполнить файл .env в соответствии с примером (пример в следующем разделе);
- запустить консоль в корневой папке приложения;
- ввести команду 'docker compose up';
- запустить еще одну консоль в той же папке;
- ввести в ней команду 'docker compose run django bash для того, чтобы "войти" в контейнер и вводить команды в его систему;
- в консоль ввести команду python manage.py createsuperuser, заполнить запрашиваемые поля;
- перейти по адресу http://127.0.0.1/admin/oauth2_provider/application/;
- создать новое приложение со следующими настройками:
    1. Client type: confidential.
    2. Authorization grant type: Resource owner password-based.
    3. Hash client secret - отключено.
- перейти по адресу http://127.0.0.1/docs/swagger/ ;
- отправить запрос на авторизацию по адресу /auth/login/token . В запрос необходимо вставить client_id и secret_key из зарегистрированного приложения. Так как проект представляет простое API, я не стал прятать его;
- скопировать token, нажать на кнопку "Authorize" справа сверху экрана, ввести токен;
- далее можно проводить тестирование.

## Пример заполнения .env файла
```
SECRET_KEY = 'django-insecure-%ny-a9jw^m+-*tqfk-aaaaaaaaaaa(pqbbbbbbbbbbbbb'

ENGINE = 'django.db.backends.postgresql_psycopg2'
POSTGRES_DB = 'referal_system'
HOST = 'db'
PORT = '5432'
POSTGRES_USER = 'postgres'
POSTGRES_PASSWORD = 'aabbccDDEE8877_'

HUNTER_API_KEY = "79e74228fd6a3f43e5b773a900b3cbd17af21247"
HUNTER_API_URL="https://api.hunter.io/v2/email-verifier"


CACHE_TIMEOUT = "60"
REDIS_URL = "redis://redis:6379/1"

GUNICORN_WORKERS = "2"
```

Пароли и secret_key заменены на нерабочие, остальные данные актуальны.
