import random

from django.core.management import BaseCommand
from faker import Faker

from app.articles.models import Article
from app.authentication.models import User

fake = Faker()
Faker.seed(0)


class Command(BaseCommand):
    help = 'Create random articles'

    def add_arguments(self, parser):
        parser.add_argument('create_size', type=int)

    def handle(self, *args, **options):
        create_size = options.get('create_size', 10)

        users = User.objects.filter(is_active=True).all()
        users_size = users.count()
        users = list(users)

        Article.objects.bulk_create(
            [
                Article(
                    title=fake.paragraph(nb_sentences=1),
                    content=fake.paragraph(nb_sentences=3),
                    creator=users[random.randint(0, users_size - 1)]
                )
                for _ in range(create_size)
            ],
            batch_size=1000,
            ignore_conflicts=True
        )
