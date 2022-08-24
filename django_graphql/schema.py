import graphene

from app.articles.mutations import (
    UpdateArticleMutation, CreateArticleMutation, DeleteArticleMutation
)
from app.articles.queries import (
    ArticleQuery,
    UserQuery,
    # CommentQuery
)


class Query(
    ArticleQuery,
    UserQuery,
    # CommentQuery,
    graphene.ObjectType
):
    pass


# class Mutation(
#     CreateArticleMutation,
#     UpdateArticleMutation,
#     DeleteArticleMutation,
#     graphene.ObjectType
# ):
#     pass


class Mutation(graphene.ObjectType):
    create_article = CreateArticleMutation.Field()
    update_article = UpdateArticleMutation.Field()
    delete_article = DeleteArticleMutation.Field()


schema = graphene.Schema(
    query=Query,
    mutation=Mutation
)
