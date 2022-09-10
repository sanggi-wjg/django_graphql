import logging

from celery import shared_task

from app.articles.models import Article
from app.authentication.models import User


@shared_task
def something_batch():
    users = User.objects.all()

    for user in users:
        text = f"Email : {user.email} name : {user.username}"
        print(text)
        logging.info(text)


@shared_task
def search_articles_like_chars():
    articles = Article.objects.filter(title__contains="ab").all()
    print("Article Count : ", articles.count())

# something_batch.delay()
