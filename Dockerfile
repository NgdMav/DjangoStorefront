# Dockerfile
# ==========
# Multi-stage build для уменьшения размера образа
# ==========

# Этап 1: Builder - установка зависимостей
FROM python:3.11-slim as builder

# Установка системных зависимостей для сборки Python пакетов
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Создание виртуального окружения
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Копирование файлов зависимостей
COPY requirements-prod.txt .

# Установка Python зависимостей
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements-prod.txt

# ==========

# Этап 2: Runtime - финальный образ
FROM python:3.11-slim

# Установка runtime зависимостей
RUN apt-get update && apt-get install -y \
    libpq-dev \
    curl \
    gettext \
    # Для Pillow (обработка изображений) \
    libjpeg-dev \
    zlib1g-dev \
    libfreetype6-dev \
    liblcms2-dev \
    libopenjp2-7-dev \
    libtiff5-dev \
    libwebp-dev \
    && rm -rf /var/lib/apt/lists/*

# Создание пользователя для безопасности
RUN groupadd -r django && useradd -r -g django -u 1000 django

# Создание директорий для приложения
RUN mkdir -p /app && chown django:django /app
WORKDIR /app

# Копирование виртуального окружения из builder
COPY --from=builder --chown=django:django /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONPATH="/app:$PYTHONPATH"

# Копирование приложения
COPY --chown=django:django . .

# Создание директорий для статики и медиа
RUN mkdir -p /app/static /app/media && \
    chown -R django:django /app/static /app/media

# Настройка порта
EXPOSE 8000

USER django

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health/ || exit 1

# Команда по умолчанию (переопределяется в docker-compose)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "storefront.wsgi:application"]