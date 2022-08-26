from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import User, AbstractUser, PermissionsMixin
from django.db import models
from django.utils.text import slugify


class ArticleManager(models.Manager):

    def create_article(self, title: str, content: str, creator_id: int):
        try:
            user = User.objects.get(pk=creator_id)
        except User.DoesNotExist:
            raise User.DoesNotExist(f"this user not exist: {creator_id}")

        new_article = self.model(
            title=title,
            content=content,
            creator=user,
        )
        new_article.save()
        return new_article


class Article(models.Model):
    objects = ArticleManager()

    title = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, allow_unicode=True, db_index=True)
    content = models.TextField()

    creator = models.ForeignKey("authentication.User", on_delete=models.CASCADE, related_name="articles")

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.slug = slugify(self.title)
        super(Article, self).save(force_insert, force_update, using, update_fields)

    @property
    def comment_count(self):
        return self.comments.count()

    @property
    def masking_creator_username(self):
        if hasattr(self, 'creator'):
            return f"".join([
                name if i % 2 == 0 else '*'
                for i, name in enumerate(list(self.creator.username))
            ])
        return ""


class CommentManager(models.Manager):

    def create_comment(self, content: str, user_id: int, article_id: int):
        try:
            article = Article.objects.get(pk=article_id)
            user = User.objects.get(pk=user_id)
        except Article.DoesNotExist:
            raise Article.DoesNotExist(f"this article not exist: {article_id}")
        except User.DoesNotExist:
            raise User.DoesNotExist(f"this user not exist: {user_id}")

        new_comment = self.model(
            content=content,
            article=article,
            creator=user
        )
        new_comment.save()
        return new_comment


class Comment(models.Model):
    objects = CommentManager()

    content = models.CharField(max_length=250)

    creator = models.ForeignKey(
        "authentication.User", on_delete=models.CASCADE, related_name="comments"
    )
    article = models.ForeignKey(
        "Article", on_delete=models.CASCADE, related_name="comments"
    )

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content
