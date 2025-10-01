# Django Tasks API (REST)

Простое REST API для управления задачами на **Django + DRF + PostgreSQL**, с валидацией, логированием, пагинацией, фильтрацией по статусу и JWT-аутентификацией.

## Стек
- Django 5
- Django REST Framework
- SimpleJWT (JWT-аутентификация)
- PostgreSQL (через `psycopg2-binary`)
- pytest (опционально) / встроенные тесты DRF
- Postman коллекция для тестирования

## Установка

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # при необходимости поправьте значения
```

## Postgres с Docker
```bash
docker compose up -d
```

## Миграции и запуск
```bash
python manage.py migrate
python manage.py createsuperuser  # по желанию
python manage.py runserver 0.0.0.0:8000
```

## JWT
Получить токен:
```
POST /api/token/
Body: {"username":"api","password":"api"}
```
Обновить токен:
```
POST /api/token/refresh/
Body: {"refresh":"<refresh token>"}
```

Для демо можно создать пользователя:
```bash
python manage.py shell -c "from django.contrib.auth import get_user_model; U=get_user_model(); U.objects.create_user('api', password='api')"
```

## Эндпоинты
- `GET /api/tasks` — список задач (пагинация `?page=1&limit=20`, фильтр `?status=pending|in_progress|done`)
- `POST /api/tasks` — создать задачу (**JWT обязателен**)
- `GET /api/tasks/{id}` — получить задачу
- `PUT /api/tasks/{id}` — обновить (**JWT обязателен**)
- `DELETE /api/tasks/{id}` — удалить (**JWT обязателен**)

## Примеры
Успех:
```json
{"count":1,"next":null,"previous":null,"results":[{"id":1,"title":"Test","description":null,"status":"pending","created_at":"2025-10-01T10:00:00Z","updated_at":"2025-10-01T10:00:00Z"}]}
```
Ошибка валидации:
```json
{"title":["Заголовок обязателен"]}
```

## Тесты
```bash
python manage.py test
```
или, если используете pytest:
```bash
pytest -q
```

## Postman
Импортируйте `postman/Tasks API.postman_collection.json`.
