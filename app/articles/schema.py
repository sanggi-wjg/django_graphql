import graphene
from django.contrib.auth.models import User
from graphene_django import DjangoObjectType

from app.articles.models import Article, Comment


class UserNode(DjangoObjectType):
    class Meta:
        model = User
        exclude = ('is_superuser', 'is_staff', 'password')


class ArticleNode(DjangoObjectType):
    greeting = graphene.String()

    class Meta:
        model = Article
        # interfaces = (relay.Node,)
        fields = (
            'id', 'title', 'slug', 'content', 'datetime_created', 'datetime_updated',
            'creator', 'comments',
            'greeting',
        )
        filter_fields = {
            'title': ['contains', 'exact'],
            'slug': ['exact', 'startswith'],
            'content': ['contains', ],
        }

    def resolve_greeting(self, info):
        return "hello"


class CommentNode(DjangoObjectType):
    class Meta:
        model = Comment
        # interfaces = (relay.Node,)
        # fields = "__all__"
        # exclude = ("datetime_updated",)
        fields = (
            'id', 'content', 'creator', 'article', 'datetime_created', 'datetime_updated'
        )
        filter_fields = {
            'content': ['contains', ],
        }


class CommentMutation(graphene.Mutation):
    class Arguments:
        comment_id = graphene.ID()
        content = graphene.String(required=True)

    comment = graphene.Field(CommentNode)

    @classmethod
    def mutate(cls, root, info, comment_id: int, content: str):
        comment = Comment.objects.get(id=comment_id)
        comment.content = content
        comment.save()
        print(root)
        print(dir(root))
        print(root.__dict__)
        print(info)
        print(dir(info))
        print(info.__dict__)
        return CommentMutation(comment=comment)


class ArticleQuery(graphene.ObjectType):
    # article = relay.Node.Field(ArticleNode)
    # article_all_by = DjangoFilterConnectionField(ArticleNode)
    # comment = relay.Node.Field(CommentNode)
    # comment_all_by = DjangoFilterConnectionField(CommentNode)

    articles = graphene.List(
        ArticleNode,
        title=graphene.String(required=False),
        content=graphene.String(required=False),
    )
    article_by_id = graphene.Field(
        ArticleNode,
        articleId=graphene.Int(required=True)
    )

    def resolve_articles(
            self, info,
            title: str = None,
            content: str = None,
    ):
        articles = Article.objects.select_related('creator').prefetch_related('comments').all()
        if title:
            articles = articles.filter(title=title)
        if content:
            articles = articles.filter(content__contains=content)

        print(articles.query)
        return articles

    def resolve_article_by_id(self, info, articleId: int):
        return Article.objects.select_related('creator').get(id=articleId)


class Mutation(graphene.ObjectType):
    update_comment = CommentMutation.Field()


article_schema = graphene.Schema(query=ArticleQuery, mutation=Mutation)
