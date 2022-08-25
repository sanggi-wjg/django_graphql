import graphene
from django.contrib.auth.models import User
from graphene import relay
from graphene_django import DjangoObjectType

from app.articles.filters import ArticleFilter, CommentFilter
from app.articles.models import Article, Comment
from app.core.base_connections import PaginationConnection
from app.core.colorful import cyan, yellow


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
        ).all()

    @classmethod
    def get_node(cls, info, id):
        queryset = cls.Meta.model.objects
        try:
            return queryset.get(pk=id)
        except queryset.DoesNotExist:
            return None

    comment_count = graphene.Int(description="글 댓글 개수")
    masking_creator_username = graphene.String(description="마스킹 된 유저 이름")

    def resolve_comment_count(self, info):
        return self.comment_count

    def resolve_masking_creator_username(self, info):
        return self.masking_creator_username


class CommentType(DjangoObjectType):
    class Meta:
        model = Comment
        # fields = ("article", "content")
        exclude = (
            "article",
        )
        filterset_class = CommentFilter
        interfaces = (relay.Node,)
        connection_class = PaginationConnection

    @classmethod
    def get_queryset(cls, queryset, info):
        # yellow(info)
        # cyan(dir(info))
        # # cyan(info.context)
        # cyan(info['article__id'])
        return queryset.select_related(
            'creator'
        ).all()

    @classmethod
    def get_node(cls, info, id):
        queryset = cls.Meta.model.objects
        try:
            return queryset.get(pk=id)
        except queryset.DoesNotExist:
            return None
