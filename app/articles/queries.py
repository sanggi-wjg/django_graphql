import graphene
from graphene_django.debug import DjangoDebug
from graphene_django.filter import DjangoFilterConnectionField
from graphql import ResolveInfo

from app.articles.models import Article, Comment
from app.articles.types import ArticleType, CommentType
from app.core.graphen_utils import get_id_from_gid


class ArticleQuery(graphene.ObjectType):
    debug = graphene.Field(DjangoDebug, name='_debug')

    # article = graphene.Field(ArticleType, article_id=graphene.ID(required=True))
    articles = DjangoFilterConnectionField(ArticleType)

    # comment = graphene.Field(CommentType, comment_id=graphene.ID(required=True))
    comments = DjangoFilterConnectionField(CommentType, article_id=graphene.ID(required=True))

    # def resolve_article(self, info: ResolveInfo, article_id: str):
    #     try:
    #         return Article.objects.get(pk=get_id_from_gid(article_id))
    #     except Article.DoesNotExist:
    #         return None
    #
    # def resolve_comment(self, info: ResolveInfo, comment_id: str):
    #     try:
    #         return Comment.objects.get(pk=get_id_from_gid(comment_id))
    #     except Comment.DoesNotExist:
    #         return None
