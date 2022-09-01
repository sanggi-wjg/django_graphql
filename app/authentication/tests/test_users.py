import sys

import pytest
from graphene.test import Client

from app.articles.models import Article
from app.authentication.models import User
from app.core.colorful import yellow


@pytest.mark.django_db
def test_users_with_article_query(client: Client):
    # given
    User.objects.create_user("test", "test@dev.com", "test123")

    # when
    users = User.objects.filter().all()
    yellow(users)

    articles = Article.objects.all()
    yellow(articles)
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
    #                 articleCount
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
