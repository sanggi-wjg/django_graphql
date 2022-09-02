import uuid

from faker import Faker

from app.authentication.models import User

fake = Faker()
Faker.seed(0)


def create_users():
    for _ in range(5):
        username = fake.name()
        User.objects.create_user(
            username + f"-{uuid.uuid4()}",
            fake.email() + f"-{uuid.uuid4()}",
            username
        )
