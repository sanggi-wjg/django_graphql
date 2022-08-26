import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from graphql import ResolveInfo

from app.authentication.models import User
from app.core.base_connections import PaginationConnection


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

    @classmethod
    def get_queryset(cls, queryset, info):
        return queryset.all()
        # return queryset.prefetch_related('articles').all()

    article_count = graphene.Int(description="유저 글 개수")

    def resolve_article_count(self: User, info: ResolveInfo):
        return self.get_article_count
