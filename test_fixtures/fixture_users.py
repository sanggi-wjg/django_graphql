import random
import uuid

from faker import Faker

from app.authentication.models import User

fake = Faker()
Faker.seed(0)


def create_users():
    for _ in range(5):
        User.objects.create_user(
            f"-{uuid.uuid4()}-{random.randint(0, 100)}",
            fake.email() + f"-{uuid.uuid4()}",
            fake.name()
        )
