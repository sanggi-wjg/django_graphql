import random
import uuid

from faker import Faker

from app.articles.models import Article
from app.authentication.models import User

fake = Faker()
Faker.seed(0)


def create_users():
    users = []
    for _ in range(5):
        users = User.objects.create_user(
            f"-{uuid.uuid4()}-{random.randint(0, 100)}",
            fake.email() + f"-{uuid.uuid4()}",
            fake.name()
        )
    yield users


def create_articles(users):
    users = list(users)
    users_size = len(users)

    Article.objects.bulk_create(
        [
            Article(
                title=fake.paragraph(nb_sentences=1),
                content=fake.paragraph(nb_sentences=3),
                creator=users[random.randint(0, users_size - 1)]
            )
            for _ in range(10)
        ],
        batch_size=1000,
        ignore_conflicts=True
    )
