import graphene

from app.articles.models import Article
from app.articles.types import ArticleType


# class BaseMutation(graphene.Mutation):
#     class Meta:
#         abstract = True
#
#     @classmethod
#     def perform_mutation(cls, root, info, **data):
#         print(root)
#         print(info)
#         print(data)


class ArticleInputBase(graphene.InputObjectType):
    title = graphene.String(required=True)
    content = graphene.String(required=True)


class CreateArticleInput(ArticleInputBase):
    creator_id = graphene.ID(required=True)


class CreateArticleMutation(graphene.Mutation):
    class Arguments:
        input = CreateArticleInput(required=True)

    article = graphene.Field(ArticleType)

    @classmethod
    def mutate(cls, root, info, input: dict):
        new_article = Article.objects.create_article(
            title=input.get('title'),
            content=input.get('content'),
            creator_id=input.get('creator_id')
        )
        return CreateArticleMutation(article=new_article)


class UpdateArticleMutation(graphene.Mutation):
    class Arguments:
        article_id = graphene.ID(required=True)
        input = ArticleInputBase(required=True)

    article = graphene.Field(ArticleType)

    @classmethod
    def mutate(cls, root, info, article_id: int, input: dict):
        try:
            article = Article.objects.get(pk=article_id)
            article.title = input.get('title', article.title)
            article.content = input.get('content', article.content)
            article.save()
        except Article.DoesNotExist:
            raise Article.DoesNotExist(f"this article not exist: {article_id}")

        return UpdateArticleMutation(article=article)


class DeleteArticleMutation(graphene.Mutation):
    class Arguments:
        article_id = graphene.ID()

    is_success = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, article_id: int):
        article = Article.objects.filter(pk=article_id)
        if not article.exists():
            raise Article.DoesNotExist(f"this article not exist: {article_id}")

        article.delete()
        return DeleteArticleMutation(is_success=True)
