from pprint import pprint

import pytest
from django.urls import reverse
from graphene.test import Client
from memory_profiler import profile
from pytest_django.asserts import assertNumQueries
from rest_framework import status
from rest_framework.test import APIClient

from app.articles.models import Article
from app.authentication.models import User
from app.core.colorful import yellow, cyan, red, green


def setup_function(function):
    red("SETUP FUNCTION")


def teardown_function(function):
    red("TEAR DOWN FUNCTION")


@pytest.mark.django_db
def test_users_query(
        query_client: Client,
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
    result = query_client.execute(query)
    # then
    green(result)


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

    with assertNumQueries(5):
        for i in range(5):
            user = users[i]

    with assertNumQueries(1):
        users = list(users)
        for i in range(5):
            user = users[i]

    something_func()


@pytest.mark.django_db
def test_is_duplicate_email_mutation(
        gql_query,
        query_client
):
    # given
    User.objects.create_user("test@dev.com", "test.dev.com", "123")
    query = """
    mutation IsDuplicateUserEmail($input:IsDuplicateEmailInput!){
      isDuplicateUserEmail(input:$input){
        isDuplicate
      }
    }
    """
    data = {
        "input": {
            "email": "123"
        }
    }

    # when
    result = query_client.execute(query, variables=data)
    # result = gql_query(query, input_data=vars)
    # then
    green(result)


@profile
def something_func():
    a = [1] * (10 ** 6)
    b = [2] * (2 * 10 ** 7)
    del b
    return a


# given
# @profile
def using_count_query():
    return User.objects.all().count()


# @profile
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
