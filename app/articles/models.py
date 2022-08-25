from django.contrib.auth.models import User
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

    creator = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="articles")

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.slug = slugify(self.title)
        super(Article, self).save(force_insert, force_update, using, update_fields)


class Comment(models.Model):
    content = models.CharField(max_length=250)

    creator = models.ForeignKey(
        "auth.User", on_delete=models.CASCADE, related_name="comments"
    )
    article = models.ForeignKey(
        "Article", on_delete=models.CASCADE, related_name="comments"
    )

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content
