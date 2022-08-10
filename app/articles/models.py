from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, allow_unicode=True)
    content = models.TextField()

    creator = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="article")

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


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
