from celery import shared_task

from app.authentication.models import User
from app.core.colorful import yellow


@shared_task
def something_batch():
    users = User.objects.all()

    for user in users:
        yellow(f"Email : {user.email} name : {user.username}")
