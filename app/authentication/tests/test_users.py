from pprint import pprint

import pytest
from django.urls import reverse
from graphene.test import Client
from line_profiler_decorator import profiler
from memory_profiler import profile
from pytest_django.asserts import assertNumQueries
from rest_framework import status
from rest_framework.test import APIClient

from app.articles.models import Article
from app.authentication.models import User
from app.core.colorful import yellow, cyan, red, green


def setup_module(module):
    red("SETUP MODULE")


def teardown_module(module):
    red("TEAR DOWN MODULE")


def setup_function(function):
    yellow("SETUP FUNCTION")


def teardown_function(function):
    yellow("TEAR DOWN FUNCTION")


@pytest.mark.django_db
def test_users_query(
        query_client: Client,
        create_random_users,
        create_superuser
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
    print()
    pprint(result)


@pytest.mark.django_db
def test_users_api_client(
        api_client: APIClient,
        create_random_users
):
    # when
    response = api_client.get(reverse('users-list'))
    # then
    assert response.status_code == status.HTTP_200_OK, "200 성공이여야 한다."
    for r in response.json():
        cyan(r)


@pytest.mark.django_db
def test_users_queryset(
        create_random_users,
        create_random_articles_with_random_users
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
    something_func_line_profile()


@pytest.mark.django_db
def test_is_duplicate_email_mutation(
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
    green(result)

    # then
    assert result.get('data'), "Success Case 이므로 성공적으로 data를 가져와야 한다."
    assert not result.get('errors'), "Success Case 이므로 errors 는 발생하지 않아야 한다."

    data = result.get('data').popitem()
    assert not data[1].get('is_duplicate'), "유저 생겅 Validate 규칙을 통해 중복은 발생해야 하지 않는다."


@profile
def something_func():
    a = [1] * (10 ** 6)
    b = [2] * (2 * 10 ** 7)
    del b
    return a


@profiler
def something_func_line_profile():
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
