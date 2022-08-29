import graphene
from django.db.models import Count
from graphene import relay
from graphene_django import DjangoObjectType
from graphql import ResolveInfo

from app.articles.loaders import ArticleCreatorCountLoader
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

    @classmethod
    def get_queryset(cls, queryset, info):
        return queryset.prefetch_related('articles').all()

    article_count = graphene.Int(description="유저 글 개수")
    my_article_count = graphene.Int(description="유저 글 개수(최적화?)")
    # 그냥 Articles 가져오기
    create_articles = graphene.List(ArticleType)
    # DataLoader 사용해서 Articles 가져오기
    loader_create_articles = graphene.List(ArticleType)

    def resolve_article_count(self: User, info: ResolveInfo):
        return self.get_article_count

    def resolve_my_article_count(self: User, info: ResolveInfo):
        article_creator_count_loader = ArticleCreatorCountLoader()
        return article_creator_count_loader.load(
            self.get_articles_queryset.prefetch_related('creator').distinct().count()
        )

    def resolve_create_articles(self: User, info: ResolveInfo):
        return self.articles.get_queryset()

    def resolve_loader_create_articles(self: User, info: ResolveInfo):
        # user_loader = UserLoader()
        # return user_loader.load(self.get_articles)
        from app.articles.loaders import ArticleLoader
        article_loader = ArticleLoader()
        return article_loader.load(self.get_articles_queryset)
