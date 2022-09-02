import uuid

import pytest
from faker import Faker
from rest_framework.test import APIClient

from graphene.test import Client

from typing import Generator, Any

from app.authentication.models import User
from test_fixtures import fixture_users


@pytest.fixture(scope='function')
def client() -> Generator[Client, Any, None]:
    """
    GraphQL Test Client
    :return: Client
    :rtype: Client
    """
    from django_graphql.schema import schema
    yield Client(schema)


@pytest.fixture(scope='function')
def api_client() -> Generator[APIClient, Any, None]:
    """
    DRF API Client
    :return APIClient
    :rtype APIClient
    """
    yield APIClient()


@pytest.fixture(scope='session')
def django_db_setup():
    """
    Override dependency django_db_setup
    """
    from django.conf import settings
    settings.DATABASE = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'db_test.sqlite3',
            # 'NAME': ':memory',
        }
    }


@pytest.fixture(scope='function')
def create_random_users():
    """
    Create Users with faker
    """
    fixture_users.create_users()
