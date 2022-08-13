import graphene
from django.contrib.auth.models import User

from app.articles.models import Comment, Article
from app.articles.nodes import CommentNode


class CreateCommentMutation(graphene.Mutation):
    comment = graphene.Field(CommentNode)

    class Arguments:
        content = graphene.String(required=True)
        creator_id = graphene.Int(required=True)
        article_id = graphene.Int(required=True)

    @classmethod
    def mutate(cls, root, info, content: str, creator_id: int, article_id: int):
        comment = Comment.objects.create(
            content=content,
            creator=User.objects.get(id=creator_id),
            article=Article.objects.get(id=article_id)
        )
        return CreateCommentMutation(comment=comment)


class UpdateCommentMutation(graphene.Mutation):
    comment = graphene.Field(CommentNode)

    class Arguments:
        comment_id = graphene.ID()
        content = graphene.String(required=True)

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
        return UpdateCommentMutation(comment=comment)


class CommentMutation(graphene.ObjectType):
    create_comment = CreateCommentMutation.Field()
    update_comment = UpdateCommentMutation.Field()
