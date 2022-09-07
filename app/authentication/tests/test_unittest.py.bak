import random
import uuid
from unittest import TestCase

from faker import Faker


from app.authentication.models import User
from app.core.colorful import red, cyan, yellow

fake = Faker()
Faker.seed(0)


class UserTestCase(TestCase):

    def setUp(self) -> None:
        red("SETUP")
        for _ in range(5):
            User.objects.create_user(
                f"-{uuid.uuid4()}-{random.randint(0, 100)}",
                fake.email() + f"-{uuid.uuid4()}",
                fake.name()
            )

    def tearDown(self) -> None:
        red("TEAR DOWN")

    def test_0001(self):
        users = User.objects.all()
        for user in users:
            cyan(user)

    def test_0002(self):
        users = User.objects.all()
        for user in users:
            yellow("--", user)
