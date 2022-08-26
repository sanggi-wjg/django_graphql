import graphene
from graphene import relay
from graphene_django.debug import DjangoDebug
from graphene_django.filter import DjangoFilterConnectionField

from app.articles.types import ArticleType, CommentType


class ArticleQuery(graphene.ObjectType):
    debug = graphene.Field(DjangoDebug, name='_debug')

    article = relay.Node.Field(ArticleType)
    articles = DjangoFilterConnectionField(ArticleType)

    comment = relay.Node.Field(CommentType)
    comments = DjangoFilterConnectionField(CommentType)
