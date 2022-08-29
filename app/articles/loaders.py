from collections import defaultdict
from typing import List

from django.db.models import Count
from graphene_django import DjangoObjectType
from promise import Promise
from promise.dataloader import DataLoader

from app.articles.models import Article
from app.authentication.models import User
from app.core.colorful import cyan


class ArticleLoader(DataLoader):

    def batch_load_fn(self, keys):
        # cyan("ArticleLoader\n", keys)
        # articles = Article.objects.filter(id__in=keys)
        # return Promise.resolve([
        #     articles.get(createor__id=key) for key in keys
        # ])
        return Promise.resolve(keys)


class ArticleCreatorCountLoader(DataLoader):
    def batch_load_fn(self, keys):
        return Promise.resolve(keys)
        # cyan([key for key in keys])
        # articles = Article.objects.in_bulk(keys)
        # return Promise.resolve([
        #     key for key in keys
        # ])


def generate_loader_by_many_to_many_key(node: DjangoObjectType, attr: str):
    class Loader(DataLoader):
        def batch_load_fn(self, keys: List[str]) -> Promise:
            results_by_ids = defaultdict(list)
            lookup = {f'{attr}__id__in': keys}

            for result in node.Meta.model.objects.filter(**lookup).iterator():
                for related in getattr(result, attr).iterator():
                    results_by_ids[related.id].append(result)

            return Promise.resolve([results_by_ids.get(id, []) for id in keys])

    return Loader


def generate_loader_by_foreign_key(node: DjangoObjectType, attr: str):
    class Loader(DataLoader):
        """
        Example case of query One Reporter to Many Articles:

        Given a list of reporter id, return: { Reporter1_id: [Article1_obj, Article2_obj, Article3_obj],... }
        The idea is that for each reporter (id), return a list of Article (obj)

        >> pprint(results_by_ids)

        defaultdict(<class 'list'>,
                    {1: [<Article: Down-sized maximized firmware>,
                        <Article: Front-line mobile system engine>,
                        <Article: Implemented high-level migration>,
                        <Article: Organized incremental collaboration>,
                        <Article: Synergized well-modulated algorithm>],
                    ...
                    5: [<Article: Automated clear-thinking firmware>,
                        <Article: Intuitive radical moderator>,
                        <Article: Phased clear-thinking forecast>,
                        <Article: Proactive optimal help-desk>,
                        <Article: Proactive responsive customer loyalty>]})
        """

        def batch_load_fn(self, keys: List[str]) -> Promise:
            results_by_ids = defaultdict(list)
            lookup = {f'{attr}__in': keys}

            # For example: Article.objects.filter(reporter_id__in=[1, 2, 3,...)
            for result in node.Meta.model.objects.filter(**lookup).iterator():
                results_by_ids[getattr(result, attr)].append(result)

            return Promise.resolve([results_by_ids.get(id, []) for id in keys])

    return Loader


def generate_loader(node: DjangoObjectType, attr: str):
    # class ReporterByIdLoader(DataLoader):
    #
    #     def batch_load_fn(self, keys: List[str]):
    #         reporters = Reporter.objects.all().in_bulk(keys)
    #         return Promise.resolve([reporters.get(reporter_id) for reporter_id in keys])
    #
    # class ArticleByIdLoader(DataLoader):
    #
    #     def batch_load_fn(self, keys: List[str]):
    #         article = Article.objects.in_bulk(keys)
    #         return Promise.resolve([article.get(key) for key in keys])

    class UserLoader(DataLoader):

        async def batch_load_fn(self, keys: List[str]):
            users = User.objects.all().in_bulk(keys)
            return Promise.resolve([
                users.get(id=user_id) for user_id in keys
            ])

    class ArticleLoader(DataLoader):

        async def batch_load_fn(self, keys: List[str]):
            articles = Article.objects.in_bulk(keys)
            return Promise.resolve([
                articles.get(key) for key in keys
            ])

    class Loader(DataLoader):

        def batch_load_fn(self, keys: List[str]):
            def with_articles(articles: list):
                user_ids = [article.creator_id for article in articles]
                return UserLoader().load_many(user_ids)

            return ArticleLoader().load_many(keys).then(with_articles)

    return Loader
