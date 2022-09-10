import logging

import celery
from celery import shared_task
from celery.utils.log import get_task_logger

from app.articles.models import Article
from app.authentication.models import User


# logger = get_task_logger(__name__)
class BaseTaskRetry(celery.Task):
    autoretry_for = (Exception, KeyError)
    retry_kwargs = {'max_retries': 5}
    retry_backoff = True


@shared_task(bind=True, base=BaseTaskRetry)
def something_batch(self):
    users = User.objects.all()

    for user in users:
        text = f"Email : {user.email}"
        print(text)
        logging.info(text)


@shared_task
def search_articles_like_chars():
    articles = Article.objects.filter(title__contains="ab").all()
    logging.info("Article Count : ", articles.count())

# something_batch.delay()
# search_articles_like_chars.run()
