from functools import partial

import graphene
from graphene import relay
from graphene_django import DjangoObjectType, DjangoConnectionField
from graphene_django.filter import DjangoFilterConnectionField
from graphql import ResolveInfo
from promise import Promise

from app.articles.types import ArticleType
from app.authentication.models import User
from app.core.base_connections import PaginationConnection


class PromiseDjangoFilterConnectionField(DjangoFilterConnectionField):

    @classmethod
    def resolve_queryset(
            cls, connection, iterable, info, args, filtering_args, filterset_class
    ):
        qs = super(DjangoFilterConnectionField, cls).resolve_queryset(
            connection, iterable, info, args
        )

        filter_kwargs = {k: v for k, v in args.items() if k in filtering_args}
        on_resolve = partial(filterset_class, data=filter_kwargs, request=info.context)

        if Promise.is_thenable(qs):
            return Promise.resolve(qs).then(lambda qs: on_resolve(queryset=qs).qs)

        return on_resolve(queryset=qs).qs


class UserType(DjangoObjectType):
    class Meta:
        model = User
        exclude = ('password', "comments")
        interfaces = (relay.Node,)
        filter_fields = {
            "username": ('exact', "contains"),
            "email": ('exact', "contains"),
        }
        connection_class = PaginationConnection

    article_count = graphene.Int(description="유저의 글 개수")

    def resolve_article_count(self: User, info: ResolveInfo):
        return info.context.loaders.article_count_by_user_id.load(self.id)

    d_articles = DjangoConnectionField(ArticleType, description="유저의 글")
    # d_articles = DjangoFilterConnectionField(ArticleType, description="유저의 글")
    # d_articles = PromiseDjangoFilterConnectionField(ArticleType, description="유저의 글")

    def resolve_d_articles(self: User, info: ResolveInfo, *args, **kwargs):
        # self.articles.filter()
        return info.context.loaders.articles_by_user_id.load(self.id)
