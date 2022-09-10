import logging

from celery import shared_task

from app.authentication.models import User


@shared_task
def something_batch():
    users = User.objects.all()

    for user in users:
        logging.info(f"Email : {user.email} name : {user.username}")


something_batch.delay()
