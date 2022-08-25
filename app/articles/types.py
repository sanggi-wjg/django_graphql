from django.contrib.auth.models import User
from graphene import relay
from graphene_django import DjangoObjectType

from app.articles.filters import ArticleFilter
from app.articles.models import Article, Comment
from app.core.base_connections import PaginationConnection


class UserType(DjangoObjectType):
    class Meta:
        model = User
        exclude = ('password', "articles", "comments")
        interfaces = (relay.Node,)
        filter_fields = {
            "username": ('exact', "contains"),
            "email": ('exact', "contains"),
        }
        connection_class = PaginationConnection


class ArticleType(DjangoObjectType):
    class Meta:
        model = Article
        filterset_class = ArticleFilter
        interfaces = (relay.Node,)
        connection_class = PaginationConnection

    @classmethod
    def get_queryset(cls, queryset, info):
        return queryset.select_related(
            'creator'
        ).prefetch_related(
            'comments', 'comments__creator',
            'comments__replied'
        ).all()


class CommentType(DjangoObjectType):
    class Meta:
        model = Comment
        # fields = ("content", "creator", "datetime_updated")
        exclude = ("article",)
        filter_fields = {
            "content": ('contains',)
        }
        interfaces = (relay.Node,)
        connection_class = PaginationConnection

    @classmethod
    def get_queryset(cls, queryset, info):
        return queryset.select_related(
            'creator'
        ).all()
