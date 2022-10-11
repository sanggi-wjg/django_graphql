import graphene
from graphene import relay
from graphene_django import DjangoObjectType, DjangoConnectionField
from graphql import ResolveInfo

from app.articles.types import ArticleType
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

    # @classmethod
    # def get_node(cls, info, id):
    #     queryset = cls.Meta.model
    #     print(queryset)
    #     try:
    #         return cls(queryset.objects.get(pk=id))
    #     except queryset.DoesNotExist:
    #         return None
    # @classmethod
    # def get_queryset(cls, queryset, info):
    #     return queryset.prefetch_related('articles').all()

    article_count = graphene.Int(description="유저 글 개수")

    def resolve_article_count(self: User, info: ResolveInfo):
        return info.context.loaders.article_count_by_user_id.load(self.id)

    articles = DjangoConnectionField(ArticleType)

    @staticmethod
    def resolve_articles(self: User, info: ResolveInfo):
        return info.context.loaders.articles_by_user_id.load(self.id)
