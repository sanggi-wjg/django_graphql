import graphene
from django.contrib.auth.models import User
from graphene_django import DjangoObjectType

from app.articles.models import Comment, Article


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
