from typing import Generator, Any

import pytest
from graphene.test import Client
from graphene_django.utils.testing import graphql_query
from rest_framework.test import APIClient

from app.authentication.models import User
from test_fixtures import fixture_users


@pytest.fixture(scope='session')
def query_client() -> Generator[Client, Any, None]:
    """
    GraphQL Test Client
    :return: Client
    :rtype: Client
    """
    from django_graphql.schema import schema
    yield Client(schema)


@pytest.fixture(scope='session')
def gql_query(client):
    def func(*args, **kwargs):
        return graphql_query(*args, **kwargs, client=client)

    return func


@pytest.fixture(scope='session')
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


@pytest.fixture
def create_superuser():
    User.objects.create_superuser(
        "raynor@dev.com",
        "raynor@dev.com",
        "passw0rd"
    )


@pytest.fixture(scope='function')
def create_random_users():
    """
    Create Users with faker
    """
    fixture_users.create_users()


@pytest.fixture(scope='function')
def create_random_articles_with_random_users():
    """
    Create Users with faker
    Create Articles with fake users
    """
    users = fixture_users.create_users()
    fixture_users.create_articles(users)

# def kakao_sender():
#     yield FakeKakaoSender()
