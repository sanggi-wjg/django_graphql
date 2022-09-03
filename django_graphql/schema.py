import graphene

from app.articles.mutations import (
    UpdateArticleMutation, CreateArticleMutation, DeleteArticleMutation,
    CreateCommentMutation, IsDuplicateEmailMutation
)
from app.articles.queries import (
    ArticleQuery,
)
from app.authentication.queries import UserQuery


class Query(
    ArticleQuery,
    UserQuery,
    # CommentQuery,
    graphene.ObjectType
):
    pass


class Mutation(graphene.ObjectType):
    create_article = CreateArticleMutation.Field()
    update_article = UpdateArticleMutation.Field()
    delete_article = DeleteArticleMutation.Field()

    create_comment = CreateCommentMutation.Field()

    is_duplicate_user_email = IsDuplicateEmailMutation.Field()


schema = graphene.Schema(
    query=Query,
    mutation=Mutation
)
