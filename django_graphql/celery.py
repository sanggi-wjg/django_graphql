from __future__ import absolute_import

import os

from celery.schedules import crontab
from django.conf import settings
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_graphql.settings')

app = Celery('raynor')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.beat_schedule = {
    'something_batch': {
        'task': 'app.authentication.tasks.something_batch',
        'schedule': crontab(minute="*/1"),
        'args': (),
        'options': {}
    },
    'search_articles_like_chars': {
        'task': 'app.authentication.tasks.search_articles_like_chars',
        'schedule': crontab(minute="*/1"),
        'args': (),
        'options': {}
    }
}

# @app.task(bind=True)
# def debug_task(self):
#     print(f'Request: {self.request!r}')
