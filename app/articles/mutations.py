import graphene

from app.articles.models import Article, Comment
from app.articles.types import ArticleType, CommentType

# class BaseMutation(graphene.Mutation):
#     class Meta:
#         abstract = True
#
#     @classmethod
#     def perform_mutation(cls, root, info, **data):
#         print(root)
#         print(info)
#         print(data)
from app.authentication.models import User


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


class IsDuplicateEmailInput(graphene.InputObjectType):
    email = graphene.String(required=True)


class IsDuplicateEmailMutation(graphene.Mutation):
    class Meta:
        description = "이메일 중복 여부"

    class Arguments:
        input = IsDuplicateEmailInput(required=True)

    is_duplicate = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, input: dict):
        try:
            User.objects.get(email=input.get('email'))
            return cls(is_duplicate=True)
        except User.DoesNotExist:
            return cls(is_duplicate=False)


class CommentInputBase(graphene.InputObjectType):
    content = graphene.String(required=True)


class CreateCommentInput(CommentInputBase):
    user_id = graphene.ID(required=True)
    article_id = graphene.ID(required=True)


class CreateCommentMutation(graphene.Mutation):
    class Arguments:
        input = CreateCommentInput(required=True)

    comment = graphene.Field(CommentType)

    @classmethod
    def mutate(cls, root, info, input: dict):
        new_comment = Comment.objects.create_comment(
            input.get('content'),
            input.get('user_id'),
            input.get('article_id')
        )
        return cls(comment=new_comment)
