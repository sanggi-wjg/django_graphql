import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from graphql import ResolveInfo

from app.articles.filters import CommentFilter, ArticleFilter
from app.articles.models import Article, Comment
from app.core.base_connections import PaginationConnection


class ArticleType(DjangoObjectType):
    class Meta:
        model = Article
        filterset_class = ArticleFilter
        interfaces = (relay.Node,)
        connection_class = PaginationConnection

    my_gid = graphene.String()
    comment_count = graphene.Int(description="글 댓글 개수")
    masking_creator_username = graphene.String(description="마스킹 된 유저 이름")

    def resolve_my_gid(self: Article, info: ResolveInfo):
        return self.gid

    def resolve_comment_count(self: "Article", info: ResolveInfo):
        return self.comment_count

    def resolve_masking_creator_username(self: "Article", info: ResolveInfo):
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
