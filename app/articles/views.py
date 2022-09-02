from django.http import HttpResponse

from django.views import View
from memory_profiler import profile

from app.articles.models import Article


class ArticleView(View):

    @profile
    def get(self, request, *args, **kwargs):
        articles = Article.objects.all()
        return HttpResponse([
            {
                'id': article.id,
                'title': article.title,
                'content': article.content,
                'created_at': article.datetime_created,
            }
            for article in articles
        ])
