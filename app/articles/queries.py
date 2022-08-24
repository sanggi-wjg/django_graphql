import graphene
from django.contrib.auth.models import User
from graphene import relay
from graphene_django.debug import DjangoDebug
from graphene_django.filter import DjangoFilterConnectionField

from app.articles.models import Article, Comment
from app.articles.types import ArticleType, UserType, CommentType


class UserQuery(graphene.ObjectType):
    user_all = graphene.List(UserType)
    users = DjangoFilterConnectionField(UserType)

    def resolve_user_all(self, info):
        return User.objects.all()


# class CommentQuery(graphene.ObjectType):
#     creator = relay.Node.Field(UserQuery)
#
#     comment_all = graphene.List(CommentType)
#
#     def resolve_comment_all(self, info):
#         comments = Comment.objects.prefetch_related(
#             'creator'
#         )
#         return comments.all()


class ArticleQuery(graphene.ObjectType):
    debug = graphene.Field(DjangoDebug, name='_debug')

    creator = relay.Node.Field(UserType)
    comment = relay.Node.Field(CommentType)
    article = relay.Node.Field(ArticleType)

    article_all = DjangoFilterConnectionField(ArticleType)

    # article_all = graphene.List(ArticleType)
    # article_by_id = graphene.Field(ArticleType)

    def resolve_article_all(self, info):
        articles = Article.objects.select_related(
            'creator'
        ).prefetch_related(
            'comments', 'comments__creator'
        )
        return articles.all()

    # def resolve_article_by_id(self, info, article_id: int):
    #     try:
    #         return Article.objects.select_related(
    #             'creator'
    #         ).prefetch_related(
    #             'comments', 'comments__creator'
    #         ).get(pk=article_id)
    #     except Article.DoesNotExist:
    #         # raise exception
    #         return None
