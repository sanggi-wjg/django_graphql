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
from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView

from app.articles.views import ArticleView
from app.authentication.views import UserAPIView
from django_graphql.schema import schema

urlpatterns = [
    path('admin/', admin.site.urls),

    path("graphql", csrf_exempt(
        GraphQLView.as_view(graphiql=settings.DEBUG, schema=schema)
    )),

    path("articles", ArticleView.as_view(), name='articles-list'),
    path("users", UserAPIView.as_view(), name='users-list'),
]
