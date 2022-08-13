import graphene

from app.articles.mutations import CommentMutation
from app.articles.queries import ArticleQuery, CommentQuery


class Query(
    ArticleQuery,
    CommentQuery,
    graphene.ObjectType
):
    pass


class Mutation(
    CommentMutation,
    graphene.ObjectType
):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
