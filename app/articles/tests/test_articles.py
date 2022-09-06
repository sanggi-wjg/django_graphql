import random

import pytest
from faker import Faker
from graphene.test import Client

from app.articles.models import Article
from app.authentication.models import User
from app.core.colorful import green


@pytest.mark.django_db
def test_users_query(query_client: Client, create_random_users):
    # given
    fake = Faker()
    Faker.seed(0)

    for i in range(5):
        username = fake.name()
        email = fake.email()
        User.objects.create_user(username + f"-{i}", email + f"-{i}", username)

    users = User.objects.filter().all()
    users = list(users)

    for _ in range(5):
        Article.objects.create_article(
            title=fake.paragraph(nb_sentences=1),
            content=fake.paragraph(nb_sentences=3),
            creator_id=users[random.randint(0, len(users) - 1)].id
        )

    # when
    users = User.objects.all()
    green(users)
    green("UsersCount:", users.count())

    articles = Article.objects.all()
    green(articles)
    green("ArticleCount:", articles.count())

    # query = """
    #         {
    #           users(first:5)
    #
    #           {
    #             pageInfo {
    #               hasNextPage
    #               hasPreviousPage
    #               startCursor
    #               endCursor
    #             }
    #             edges {
    #               node {
    #                 id
    #                 username
    #                 email
    #                 is_active
    #                 is_staff
    #               }
    #               cursor
    #             }
    #             totalCount
    #             edgeCount
    #           }
    #         }
    #         """
    # result = query_client.execute(query)
    # print(result)


@pytest.mark.django_db
def test_articles():
    green("=========[TEST_ARTICLES]=================")
    users = User.objects.all()
    green(users)
    green("UsersCount:", users.count())

    articles = Article.objects.all()
    green(articles)
    green("ArticleCount:", articles.count())
    green("============================================")


def test_health_check_success_case():
    from app.articles.services import health_check_naver

    is_healthy = health_check_naver()
    assert is_healthy


def test_health_check_fail_404_case(mocker):
    from rest_framework import status
    from app.articles.services import health_check_naver

    mocker.patch(
        'app.articles.services.request_naver',
        return_value={
            'status_code': status.HTTP_404_NOT_FOUND,
            'detail': "success",
        }
    )
    is_healthy = health_check_naver()
    assert not is_healthy
