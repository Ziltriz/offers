# Используем официальный образ Python
FROM python:3.11-slim

# Устанавливаем переменные окружения
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем зависимости
COPY requirements.txt /app/

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt


# Копируем проект
COPY . /app/

RUN python manage.py collectstatic --noinput
# Команда для запуска приложения
CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000"]