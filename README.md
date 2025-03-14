# Сервис анализа навыков из HH.ru

## Цель проекта

Разработать REST API на Django Rest Framework (DRF), которое собирает вакансии с HH.ru и анализирует количество упоминаний навыков в вакансиях. Проект предоставляет возможность получать статистику по ключевым навыкам для различных профессий, что помогает понять, какие навыки наиболее востребованы на рынке труда.

---

## Функционал

### Сбор вакансий
- Проект собирает вакансии с HH.ru по заданным поисковым запросам.
- Для каждой профессии (например, Python Developer, Frontend Developer) задается отдельный поисковый запрос.

### Анализ ключевых навыков
- Для каждой вакансии извлекаются ключевые навыки.
- Подсчитывается количество упоминаний каждого навыка в вакансиях.

### REST API
- API предоставляет эндпоинты для получения списка ключевых навыков и их частоты упоминаний для каждой профессии.

### Асинхронная обработка
- Используется Celery для асинхронного сбора и обработки данных.
- Каждая вакансия обрабатывается отдельной задачей, что ускоряет выполнение.

### Админка Django
- Все модели (вакансии, профессии, ключевые навыки) доступны для управления через админку Django.

---

## Настройка проекта

### 1. Файл `.env`

Создайте файл `.env` в корне проекта и добавьте в него следующие переменные:

```env
# Настройки базы данных PostgreSQL
DB_NAME=hh_analysis
DB_USER=user
DB_PASS=password
DB_HOST=db
DB_PORT=5432

# Настройки Redis
REDIS_HOST=redis
REDIS_PORT=6379

# Настройки Django
SECRET_KEY=your-secret-key
DEBUG=True

# Порт для Django
PORT_WEB=8000
```

---


### 2.Зависимости

Убедитесь, что у вас установлены все зависимости. Для этого выполните:
```
pip install -r requirements.txt

```
### 3. Запуск через Docker


## 1. Сборка и запуск контейнеров

# Соберите и запустите контейнеры:
```
docker-compose up --build
```

# Примените миграции:
```
docker-compose exec web python manage.py migrate
```
# Создайте суперпользователя (опционально):
```
docker-compose exec web python manage.py createsuperuser
```
# Соберите статические файлы:
```
docker-compose exec web python manage.py collectstatic --noinput
```

### 4. Доступ к приложению

Django: http://localhost:8000
Админка Django: http://localhost:8000/admin

## API:

# Получить список ключевых навыков для профессии: GET /api/profession/<profession_id>/skills/


Пример: GET /api/profession/1/skills/ (для Python Developer)


### 5. Запуск Celery

## Celery автоматически запускается вместе с контейнером celery. Если нужно запустить его вручную:
```
docker-compose exec celery celery -A hh_analysis worker --loglevel=info
```

### 6. Структура проекта

hh_analysis/
├── hh_analysis/
│   ├── __init__.py
│   ├── asgi.py
│   ├── celery.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── vacancies/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── tasks.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── .env
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── manage.py
├── requirements.txt
└── README.md


### Примеры запросов к API

## 1. Получить данные по вакансиям

# Запрос:


GET /api/fetch_vacancies/<int:profession_id>/


# Описание:

Отправляется асинхронная задача на парсинг вакансий через Celery.
Предварительно необходимо создать объект профессий через админку или другим способом, указав поисковой запрос.

## 2. Получить список ключевых навыков для профессии

# Запрос:


GET /api/profession/1/skills/


#Ответ:
```
json
{
"profession": "Python Developer",
"skills": [
    {"name": "Python", "count": 10},
    {"name": "Django", "count": 8},
    {"name": "Flask", "count": 5},
    {"name": "SQL", "count": 3}
]
}

```
### 7. Технологии

Django: Основной фреймворк для создания REST API.
Django Rest Framework (DRF):     Для создания RESTful API.
Celery: Для асинхронной обработки задач.
Redis: Брокер сообщений для Celery.
PostgreSQL: База данных для хранения вакансий и навыков.
Docker: Для контейнеризации и удобного развертывания.
