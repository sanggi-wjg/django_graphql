import graphene
from graphene_django.debug import DjangoDebug

from app.articles.models import Article, Comment
from app.articles.nodes import ArticleNode, CommentNode


class ArticleQuery(graphene.ObjectType):
    # article = relay.Node.Field(ArticleNode)
    # article_all_by = DjangoFilterConnectionField(ArticleNode)
    # comment = relay.Node.Field(CommentNode)
    # comment_all_by = DjangoFilterConnectionField(CommentNode)
    debug = graphene.Field(DjangoDebug, name='_debug')
    articles = graphene.List(
        ArticleNode,
        title=graphene.String(required=False),
        content=graphene.String(required=False),
        limit=graphene.Int(required=False),
        offset=graphene.Int(required=False),
    )
    article_by_id = graphene.Field(
        ArticleNode,
        articleId=graphene.Int(required=True)
    )

    def resolve_articles(
            self, info,
            title: str = None,
            content: str = None,
            limit: int = 0,
            offset: int = 10
    ):
        articles = Article.objects.select_related('creator').prefetch_related('comments', 'comments__creator')
        if title:
            articles = articles.filter(title__contains=title)
        if content:
            articles = articles.filter(content__contains=content)

        return articles.all()[limit:offset]

    def resolve_article_by_id(self, info, articleId: int):
        return Article.objects.select_related('creator').get(id=articleId)


class CommentQuery(graphene.ObjectType):
    comments = graphene.List(
        CommentNode,
        content=graphene.String(required=False),
    )

    def resolve_comments(self, info, content: str = None):
        comments = Comment.objects.all()
        if content:
            comments = comments.filter(content__contains=content)

        return comments
