import uuid

import pytest
from faker import Faker

from graphene.test import Client

from typing import Generator, Any

from app.authentication.models import User


@pytest.fixture(scope='function')
def client() -> Generator[Client, Any, None]:
    """
    GraphQL Test Client
    :return:
    :rtype:
    """
    from django_graphql.schema import schema
    yield Client(schema)


@pytest.fixture(scope='session', autouse=True)
def django_db_setup():
    from django.conf import settings
    settings.DATABASE = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'db_test.sqlite3',
            # 'NAME': ':memory',
        }
    }


@pytest.fixture(scope='function')
def create_random_user():
    """
    Create User with faker
    :return:
    :rtype:
    """
    fake = Faker()
    Faker.seed(0)

    for _ in range(5):
        username = fake.name()
        User.objects.create_user(
            username + f"-{uuid.uuid4()}",
            fake.email() + f"-{uuid.uuid4()}",
            username
        )
