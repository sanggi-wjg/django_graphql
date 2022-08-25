import graphene
from graphene import relay
from graphene_django.debug import DjangoDebug
from graphene_django.filter import DjangoFilterConnectionField

from app.articles.types import ArticleType, UserType, CommentType


class UserQuery(graphene.ObjectType):
    user_all = graphene.List(UserType)
    users = DjangoFilterConnectionField(UserType)


class ArticleQuery(graphene.ObjectType):
    debug = graphene.Field(DjangoDebug, name='_debug')

    creator = relay.Node.Field(UserType)
    comment = relay.Node.Field(CommentType)
    article = relay.Node.Field(ArticleType)

    article_all = DjangoFilterConnectionField(ArticleType)
    comments_by = DjangoFilterConnectionField(CommentType)
