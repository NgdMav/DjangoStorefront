# Django store

## Main command:
```text
python manage.py runserver
```

## Sending and managing emails:
```text
docker run --rm -it -p 5000:80 -p 2525:25 -p 110:110 rnwood/smtp4dev
```

## Celery and redis for handling background tasks:
```text
sudo docker run -d -p 6379:6379 redis

celery -A storefront worker --loglevel=info
celery -A storefront flower
celery -A storefront beat
```

## Locust and silk for performance testing:
```text
locust -f locustfiles/browse_products.py 
```

## Redis for caching hard data:
```text
sudo docker run -d -p 6379:6379 redis

sudo docker exec -it *cont* redis-cli
select 2
keys *
flushall // for deleting all keys
```