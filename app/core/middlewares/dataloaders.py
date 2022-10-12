from collections import defaultdict

from django.db.models import Count
from graphene_django import DjangoObjectType
from promise import Promise
from promise.dataloader import DataLoader

from app.articles.filters import ArticleFilter
from app.articles.models import Article

"""
https://jerrynsh.com/solving-n-1-in-graphql-python-with-dataloader/
https://gist.github.com/ngshiheng/35b5f067350e17e568c9dfbc011e8d8b
"""


# def generate_loader(Type: DjangoObjectType, attr: str):
#
#     class ReporterByIdLoader(DataLoader):
#
#         def batch_load_fn(self, keys):
#             reporters = Reporter.objects.all().in_bulk(keys)
#             return Promise.resolve([reporters.get(reporter_id) for reporter_id in keys])
#
#     class ArticleByIdLoader(DataLoader):
#
#         def batch_load_fn(self, keys):
#             article = Article.objects.in_bulk(keys)
#             return Promise.resolve([article.get(key) for key in keys])
#
#     class Loader(DataLoader):
#         """
#         Example case of query Many Articles to One Reporter for each Article
#         """
#
#         def batch_load_fn(self, keys):
#             def with_articles(articles):
#                 reporter_ids = [article.reporter_id for article in articles]
#                 return ReporterByIdLoader().load_many(reporter_ids)
#
#             return ArticleByIdLoader().load_many(keys).then(with_articles)
#
#     return Loader


def generate_loader_by_foreign_key(model_type: DjangoObjectType, field: str):
    class Loader(DataLoader):
        """
        Example case of query One Reporter to Many Articles
        """

        def batch_load_fn(self, keys: list) -> Promise:
            results_by_ids = defaultdict(list)
            lookup = {f'{field}__in': keys}

            # For example: Article.objects.filter(reporter_id__in=[1, 2, 3,...)
            for result in model_type._meta.model.objects.filter(**lookup).iterator():
                results_by_ids[getattr(result, field)].append(result)

            return Promise.resolve([results_by_ids.get(key, []) for key in keys])

    return Loader


class DataLoaderBase(DataLoader):

    def __init__(
            self, batch_load_fn=None, batch=None, max_batch_size=None, cache=None, get_cache_key=None,
            cache_map=None, scheduler=None, **kwargs):
        super().__init__(batch_load_fn, batch, max_batch_size, cache, get_cache_key, cache_map, scheduler)
        self.kwargs = kwargs


class ArticlesByUserIdLoader(DataLoaderBase):

    def batch_load_fn(self, user_ids):
        article_by_user_id = defaultdict(list)

        qs = ArticleFilter(self.kwargs, Article.objects.filter(creator_id__in=user_ids)).qs
        for article in qs.iterator():
            # for article in Article.objects.filter(creator_id__in=user_ids).iterator():
            article_by_user_id[article.creator_id].append(article)

        return Promise.resolve([
            article_by_user_id.get(user_id, []) for user_id in user_ids
        ])


class ArticleCountByUserIdLoader(DataLoaderBase):

    def batch_load_fn(self, user_ids):
        article_counts = Article.objects.values('creator_id').filter(
            creator_id__in=user_ids
        ).annotate(count=Count('creator_id'))

        # TODO refactoring
        def get_article_count(creator_id: int) -> int:
            for count in article_counts:
                if count['creator_id'] == creator_id:
                    return count['count']
            return 0

        article_count_by_user_id = defaultdict(int)
        for user_id in user_ids:
            article_count_by_user_id[user_id] = get_article_count(user_id)

        return Promise.resolve([
            article_count_by_user_id.get(user_id, 0) for user_id in user_ids
        ])


class DataLoaders:

    def __init__(self):
        # self.articles_by_user_id = generate_loader_by_foreign_key(ArticleType, 'creator_id')
        self.articles_by_user_id = ArticlesByUserIdLoader
        self.article_count_by_user_id = ArticleCountByUserIdLoader


class DataLoaderMiddleware:

    def resolve(self, next, root, info, **kwargs):
        if not hasattr(info.context, 'loaders'):
            info.context.loaders = DataLoaders()

        return next(root, info, **kwargs)
