from django.contrib import admin

from app.articles.models import Article, Comment

admin.site.register(Article)
admin.site.register(Comment)

