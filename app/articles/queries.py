import graphene
from graphene_django.debug import DjangoDebug
from graphene_django.filter import DjangoFilterConnectionField

from app.articles.types import ArticleType, CommentType


class ArticleQuery(graphene.ObjectType):
    debug = graphene.Field(DjangoDebug, name='_debug')

    article = graphene.Field(ArticleType, article_id=graphene.ID(required=True))
    articles = DjangoFilterConnectionField(ArticleType)

    comment = graphene.Field(CommentType, comment_id=graphene.ID(required=True))
    comments = DjangoFilterConnectionField(CommentType, article_id=graphene.ID(required=True))
