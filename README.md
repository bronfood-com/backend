# бронфуд.ком
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![REST API](https://img.shields.io/badge/-REST%20API-464646?style=flat-square&logo=REST%20API)](https://restfulapi.net/)
[![PostgreSQL](https://img.shields.io/badge/-SQLite-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)

Friday-13 является сервисом для работы в кандидатами и резюме.

## Над проектом работали:
- [Александр Солодников](https://github.com/Solodnikov)
- [Витас Вакаускас](https://github.com/Qerced)
- [Владимир Толстопятов](https://github.com/syberflea)
- [Евгений Андронов](https://t.me/folite999)

## Проект можно посмотреть по адресу:
...
## Подготовка и запуск проекта
### Склонировать репозиторий на локальную машину:
```
git clone https://github.com/bronfood-com/backend
```

### Запуск проекта в контейнере:

```
docker-compose -f docker-compose.yml up -d
```

### Запуск проекта локального сервера:

```
py -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd src/
python manage.py runserver
```
## Использованые фреймворки и библиотеки:
- [Django](https://www.djangoproject.com/)
- [Django REST framework](https://www.django-rest-framework.org/)
- [django-filter](https://django-filter.readthedocs.io/en/stable/)
- [django-cors-headers](https://github.com/adamchainz/django-cors-headers)
- [Djoser](https://djoser.readthedocs.io/)
- [drf-nested-routers](https://github.com/alanjds/drf-nested-routers)
- [drf-yasg](https://drf-yasg.readthedocs.io/en/stable/)
- [Gunicorn](https://gunicorn.org/)

## Первичная документация:
```
https://localhost:8000/api/redoc

https://localhost:8000/api/swagger
```

## Работа с API через Postman Agent
...