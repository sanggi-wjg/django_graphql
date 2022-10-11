"""django_graphql URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from functools import cached_property

from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView

from app.articles.views import ArticleView
from app.authentication.views import UserAPIView
from app.aws.views import S3StorageView
from app.core.dataloaders import ArticlesByUserIdLoader, ArticleCountByUserIdLoader
from django_graphql.schema import schema


class GQLContext:
    def __init__(self, request):
        self.request = request

    @cached_property
    def user(self):
        return self.request.user

    @cached_property
    def articles_by_user_id_loader(self):
        return ArticlesByUserIdLoader()

    @cached_property
    def article_count_by_user_id_loader(self):
        return ArticleCountByUserIdLoader()


class CustomGraphQLView(GraphQLView):

    def get_context(self, request):
        return GQLContext(request)


urlpatterns = [
    path('admin/', admin.site.urls),

    path("graphql", csrf_exempt(
        CustomGraphQLView.as_view(graphiql=settings.DEBUG, schema=schema)
    )),

    path("articles", ArticleView.as_view(), name='articles-list'),
    path("users", UserAPIView.as_view(), name='users-list'),

    path("aws/s3", S3StorageView.as_view(), name='aws-s3'),
]
