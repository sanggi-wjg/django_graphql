import graphene
from django.contrib.auth.models import User
from graphene import relay
from graphene_django import DjangoObjectType

from app.articles.colorful import yellow, cyan
from app.articles.filters import ArticleFilter
from app.articles.models import Article, Comment


class UserType(DjangoObjectType):
    class Meta:
        model = User
        exclude = ('password', "articles", "comments")
        interfaces = (relay.Node,)
        filter_fields = {
            "username": ('exact', "contains"),
            "email": ('exact', "contains"),
        }


class PaginationConnection(graphene.Connection):
    class Meta:
        abstract = True

    total_count = graphene.Int()
    edge_count = graphene.Int()

    @classmethod
    def resolve_total_count(cls, root, info, **kwargs):
        return root.length

    @classmethod
    def resolve_edge_count(cls, root, info, **kwargs):
        return len(root.edges)


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
