# Используем официальный образ Python
FROM python:3.11-slim

# Установка переменных среды
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    PATH="/root/.local/bin:$PATH"

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    libpq-dev \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && apt-get clean

# Установка рабочей директории
WORKDIR /app

# Копируем зависимости и устанавливаем
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root

# Копируем весь код
COPY . .

# Команда по умолчанию: запустить сервер
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
