import pytest
from django.urls import reverse
from graphene.test import Client
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
              users(first:5)

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
    yellow(result)


@pytest.mark.django_db
def test_users_api_client(
        api_client: APIClient,
        create_random_users
):
    # when
    response = api_client.get(reverse('users-list'))
    # then
    assert response.status_code == status.HTTP_200_OK
    cyan(response.json())


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
