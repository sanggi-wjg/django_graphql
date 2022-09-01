import pytest
from faker import Faker

from graphene.test import Client

from typing import Generator, Any

from app.authentication.models import User


@pytest.fixture
def client() -> Generator[Client, Any, None]:
    from django_graphql.schema import schema
    yield Client(schema)


@pytest.fixture(scope='session')
def django_db_setup():
    from django.conf import settings
    settings.DATABASE = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'db_test.sqlite3',
            # 'NAME': ':memory',
        }
    }


@pytest.fixture
def create_basic_user():
    fake = Faker()
    Faker.seed(0)

    for i in range(10, 15):
        username = fake.name()
        email = fake.email()
        User.objects.create_user(username + f"-{i}", email + f"-{i}", username)
