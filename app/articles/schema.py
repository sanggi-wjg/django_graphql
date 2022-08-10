import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from app.articles.models import Article, Comment


class ArticleNode(DjangoObjectType):
    class Meta:
        model = Article
        interfaces = (relay.Node,)
        fields = (
            'id', 'title', 'slug', 'content', 'datetime_created', 'datetime_updated',
            'creator', 'comments',
        )
        filter_fields = {
            'title': ['contains', 'exact'],
            'slug': ['exact', 'startswith'],
            'content': ['contains', ],
        }


class CommentNode(DjangoObjectType):
    class Meta:
        model = Comment
        interfaces = (relay.Node,)
        fields = (
            'id', 'content', 'creator', 'article', 'datetime_created', 'datetime_updated'
        )
        filter_fields = {
            'content': ['contains', ],
        }


class ArticleQuery(graphene.ObjectType):
    article = relay.Node.Field(ArticleNode)
    article_all_by = DjangoFilterConnectionField(ArticleNode)

    comment = relay.Node.Field(CommentNode)
    comment_all_by = DjangoFilterConnectionField(CommentNode)

    # article_all_by = graphene.List(
    #     ArticleNode,
    #     title=graphene.String(required=False),
    #     content=graphene.String(required=False),
    # )

    # def resolve_article_all_by(
    #         self, info,
    #         title: str = None,
    #         content: str = None,
    # ):
    #     articles = Article.objects.select_related('creator').prefetch_related('comments').all()
    #     if title:
    #         articles = articles.filter(title=title)
    #     if content:
    #         articles = articles.filter(content__contains=content)
    #
    #     print(articles.query)
    #     return articles
