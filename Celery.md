
## Celery
```shell
celery -A django_graphql worker -l INFO
```

## Celery beat
```shell
celery -A django_graphql worker -l INFO -B --scheduler django_celery_beat.schedulers:DatabaseScheduler
```