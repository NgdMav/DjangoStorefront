#!/bin/bash
# docker-entrypoint.sh

set -e

# Функция для ожидания сервисов
wait_for_service() {
  local host=$1
  local port=$2
  local timeout=${3:-30}

  echo "Waiting for $host:$port..."

  for i in $(seq 1 $timeout); do
    if nc -z $host $port >/dev/null 2>&1; then
      echo "$host:$port is available!"
      return 0
    fi
    echo "Waiting for $host:$port... ($i/$timeout)"
    sleep 1
  done

  echo "Timeout waiting for $host:$port"
  return 1
}

# Ожидание PostgreSQL
wait_for_service postgres 5432 60

# Ожидание Redis
wait_for_service redis 6379 30

# Применение миграций
echo "Applying database migrations..."
python manage.py migrate --noinput

# Сбор статических файлов
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Создание суперпользователя если не существует
echo "Creating superuser if needed..."
python manage.py create_superuser_if_not_exists \
  --username=admin \
  --email=admin@storefront.com \
  --password=admin

# Загрузка начальных данных
echo "Loading initial data..."
python manage.py loaddata fixtures/initial_data.json 2>/dev/null || true

# Создание health check endpoint если не существует
if [ ! -f store/views/health.py ]; then
  echo "Creating health check endpoint..."
  cat > store/views/health.py << 'EOF'
from django.http import JsonResponse
from django.db import connection
from django.core.cache import cache

def health_check(request):
    # Проверка базы данных
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            db_ok = True
    except:
        db_ok = False

    # Проверка кеша
    cache_ok = False
    try:
        cache.set('health_check', 'ok', 5)
        cache_ok = cache.get('health_check') == 'ok'
    except:
        pass

    status = 200 if db_ok and cache_ok else 503
    return JsonResponse({
        'status': 'healthy' if status == 200 else 'unhealthy',
        'database': 'ok' if db_ok else 'error',
        'cache': 'ok' if cache_ok else 'error',
        'timestamp': datetime.now().isoformat()
    }, status=status)
EOF
fi

# Запуск команды
exec "$@"