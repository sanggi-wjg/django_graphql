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
        return UpdateCommentMutation(comment=comment)


class DeleteCommuteMutation(graphene.Mutation):
    comment = graphene.Field(CommentNode)

    class Arguments:
        comment_id = graphene.ID()

    @classmethod
    def mutate(cls, root, info, comment_id: int):
        comment = Comment.objects.get(id=comment_id)
        comment.content = "삭제된 댓글 입니다."
        comment.save()
        return DeleteCommuteMutation(comment)


class CommentMutation(graphene.ObjectType):
    create_comment = CreateCommentMutation.Field()
    update_comment = UpdateCommentMutation.Field()
    delete_comment = DeleteCommuteMutation.Field()

# class CommentMutation(SerializerMutation):
#     class Meta:
#         serializer_class = CommentSerializer
#         model_operation = ('create', 'update')
#         lookup_field = 'id'
