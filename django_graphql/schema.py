import graphene
from graphene_django.debug import DjangoDebug

from app.articles.schema import ArticleQuery
from app.ingredients.schema import Query


class Query(
    # ArticleQuery,
    Query,
    graphene.ObjectType
):
    debug = graphene.Field(DjangoDebug, name="_debug")


schema = graphene.Schema(query=Query)
