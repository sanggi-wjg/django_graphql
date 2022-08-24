from django.contrib.auth.models import User
from graphene import relay
from graphene_django import DjangoObjectType

from app.articles.models import Article, Comment


class UserType(DjangoObjectType):
    class Meta:
        model = User
        exclude = ('password', "articles", "comments")
        interfaces = (relay.Node,)
        filter_fields = ('username', "email")

    # def get_queryset(cls, queryset, info):
    #     return queryset.select_related(
    #         'creator'
    #     ).prefetch_related(
    #         'comments', 'comments__creator'
    #     )


class ArticleType(DjangoObjectType):
    class Meta:
        model = Article
        # fields = "__all__"
        # fields = (
        #     "title", "slug", "content", "datetime_created", "datetime_updated"
        # )
        filter_fields = {
            "title": ('exact', "contains"),
            "content": ('exact', "contains"),
        }
        interfaces = (relay.Node,)


class CommentType(DjangoObjectType):
    class Meta:
        model = Comment
        # fields = ("content", "creator", "datetime_updated")
        filter_fields = {
            "content": ('contains',)
        }
        interfaces = (relay.Node,)
