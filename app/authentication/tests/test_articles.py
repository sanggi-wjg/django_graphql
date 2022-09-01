import random

import pytest
from faker import Faker
from graphene.test import Client

from app.articles.models import Article
from app.authentication.models import User
from app.core.colorful import cyan


@pytest.mark.django_db
def test_users_query(client: Client, create_basic_user):
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
    cyan(users)

    articles = Article.objects.all()
    cyan(articles)

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
    # result = client.execute(query)
    # print(result)
