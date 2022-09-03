from pprint import pprint

import pytest
from django.urls import reverse
from graphene.test import Client
from memory_profiler import profile
from rest_framework import status

from rest_framework.test import APIClient
from app.articles.models import Article
from app.authentication.models import User
from app.core.colorful import yellow, cyan


@pytest.mark.django_db
def test_users_query(
        client: Client,
        create_random_users
):
    # given
    query = """
            {
              users
              {
                pageInfo {
                  hasNextPage
                  hasPreviousPage
                  startCursor
                  endCursor
                }
                edges {
                  node {
                    id
                    username
                    email
                    articleCount
                  }
                  cursor
                }
                totalCount
                edgeCount
              }
            }
            """
    # when
    result = client.execute(query)
    # then
    pprint(result)


@pytest.mark.django_db
def test_users_api_client(
        api_client: APIClient,
        create_random_users
):
    # when
    response = api_client.get(reverse('users-list'))
    # then
    assert response.status_code == status.HTTP_200_OK
    for r in response.json():
        cyan(r)


@pytest.mark.django_db
def test_users_queryset(
        create_random_users
):
    # given
    # when
    users = User.objects.all()
    yellow(users)
    yellow("UsersCount:", users.count())

    articles = Article.objects.all()
    yellow(articles)
    yellow("ArticleCount:", articles.count())

    user_count = using_count_query()
    user_count_2 = using_len_api()


# given
@profile
def using_count_query():
    return User.objects.all().count()


@profile
def using_len_api():
    return len(User.objects.all())


@pytest.mark.django_db
def test_using_count_query(
        create_random_users,
        benchmark
):
    # when
    benchmark(using_count_query)
    # then
    assert True


@pytest.mark.django_db
def test_using_len_api(
        create_random_users,
        benchmark
):
    # when
    benchmark(using_len_api)
    # then
    assert True
