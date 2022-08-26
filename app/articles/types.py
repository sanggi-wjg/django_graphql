import graphene
from graphene import relay
from graphene_django import DjangoObjectType, DjangoConnectionField
from graphql import ResolveInfo

from app.articles.filters import ArticleFilter, CommentFilter
from app.articles.models import Article, Comment, User
from app.authentication.types import UserType
from app.core.base_connections import PaginationConnection


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

    dataloader_user = graphene.Field(UserType)

    def resolve_comment_count(self: "Article", info: ResolveInfo):
        return self.comment_count

    def resolve_masking_creator_username(self: "Article", info: ResolveInfo):
        return self.masking_creator_username

    async def resolve_articles(self: "User", info: ResolveInfo):
        return info.context.loaders.user_by_article.load(self.id)
        # user_loader = UserLoader()
        # return await user_loader.load(self.id)


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
