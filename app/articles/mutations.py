import graphene
from django.contrib.auth.models import User

from app.articles.models import Article
from app.articles.types import ArticleType


class CreateArticleMutation(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        content = graphene.String(required=True)
        creator_id = graphene.ID()

    article = graphene.Field(ArticleType)

    @classmethod
    def mutate(cls, root, info, title: str, content: str, creator_id: int):
        new_article = Article.objects.create_article(
            title, content, creator_id
        )
        return CreateArticleMutation(article=new_article)


class UpdateArticleMutation(graphene.Mutation):
    class Arguments:
        article_id = graphene.ID()
        content = graphene.String(required=True)

    article = graphene.Field(ArticleType)

    @classmethod
    def mutate(cls, root, info, article_id: int, content: str):
        try:
            article = Article.objects.get(pk=article_id)
            article.content = content
            article.save()
        except Article.DoesNotExist:
            # raise exception
            raise Article.DoesNotExist("1231231231")
        return UpdateArticleMutation(article=article)


class DeleteArticleMutation(graphene.Mutation):
    class Arguments:
        article_id = graphene.ID()

    # 204 No Content?
    # 204 No Content?
    success = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, article_id: int):
        article = Article.objects.filter(pk=article_id)
        if not article.exists():
            # raise exception
            return False

        article.delete()
        return True
