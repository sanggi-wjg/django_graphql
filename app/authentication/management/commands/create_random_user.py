from django.core.management import BaseCommand
from faker import Faker

from app.authentication.models import User
from app.core.colorful import red

fake = Faker()
Faker.seed(0)


class Command(BaseCommand):
    help = 'Create random articles'

    def add_arguments(self, parser):
        parser.add_argument('create_size', type=int)

    def handle(self, *args, **options):
        create_size = options.get('create_size', 10)

        for _ in range(create_size):
            username = fake.name()
            email = fake.email()

            try:
                User.objects.get(
                    username=username,
                    email=email
                )
                red(f"User already exist: {username}")
            except User.DoesNotExist:
                User.objects.create_user(
                    username=username,
                    email=email,
                    password=username
                )
