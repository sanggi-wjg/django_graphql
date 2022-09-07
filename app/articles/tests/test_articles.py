import random

import pytest
from faker import Faker
from graphene.test import Client

from app.articles.models import Article
from app.authentication.models import User
from app.core.colorful import green


@pytest.mark.django_db
def test_something_anything_query(
        query_client: Client,
        create_random_users
):
    # given
    fake = Faker()
    Faker.seed(0)

    for i in range(5):
        username = fake.name()
        email = fake.email()
        User.objects.create_user(username + f"-{i}", email + f"-{i}", username)

    users = User.objects.all()
    users_size = users.count()
    users = list(users)
    green(users)
    green("UsersCount:", users_size)

    Article.objects.bulk_create(
        [
            Article(
                title=fake.paragraph(nb_sentences=1),
                content=fake.paragraph(nb_sentences=3),
                creator=users[random.randint(0, users_size - 1)]
            )
            for _ in range(10)
        ],
        batch_size=1000,
        ignore_conflicts=True
    )

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
def test_articles(
        create_random_articles_with_random_users
):
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
    assert is_healthy, "Naver Request 실패"


def test_health_check_fail_404_case(mocker):
    from rest_framework import status
    from app.articles.services import health_check_naver

    mocker.patch(
        'app.articles.services.request_naver',
        return_value={
            'status_code': status.HTTP_404_NOT_FOUND,
            'detail': "not found",
        }
    )
    is_healthy = health_check_naver()
    assert not is_healthy, "Naver Request는 404 에러가 발생해야 한다."
