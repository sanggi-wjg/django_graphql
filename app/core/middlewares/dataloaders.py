from collections import defaultdict

from django.db.models import Count
from graphene_django import DjangoObjectType
from promise import Promise
from promise.dataloader import DataLoader

from app.articles.models import Article


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


def generate_loader_by_foreign_key(model_type: DjangoObjectType, attr: str):
    class Loader(DataLoader):
        """
        Example case of query One Reporter to Many Articles
        """

        def batch_load_fn(self, keys: list) -> Promise:
            results_by_ids = defaultdict(list)
            lookup = {f'{attr}__in': keys}

            # For example: Article.objects.filter(reporter_id__in=[1, 2, 3,...)
            for result in model_type._meta.model.objects.filter(**lookup).iterator():
                results_by_ids[getattr(result, attr)].append(result)

            return Promise.resolve([results_by_ids.get(id, []) for id in keys])

    return Loader


class ArticlesByUserIdLoader(DataLoader):

    def batch_load_fn(self, user_ids):
        article_by_user_id = defaultdict(list)

        for article in Article.objects.filter(creator_id__in=user_ids).iterator():
            article_by_user_id[article.creator_id].append(article)

        return Promise.resolve([
            article_by_user_id.get(user_id, []) for user_id in user_ids
        ])


class ArticleCountByUserIdLoader(DataLoader):

    def batch_load_fn(self, user_ids):
        article_count_by_user_id = defaultdict(int)
        article_counts = Article.objects.values('creator_id').filter(
            creator_id__in=user_ids
        ).annotate(count=Count('creator_id'))

        def get_article_count(user_id: int) -> int:
            # TODO refactoring
            for article_count in article_counts:
                if article_count['creator_id'] == user_id:
                    return article_count['count']
            return 0

        for user_id in user_ids:
            article_count_by_user_id[user_id] = get_article_count(user_id)

        return Promise.resolve([
            article_count_by_user_id.get(user_id, []) for user_id in user_ids
        ])


class DataLoaders:

    def __init__(self):
        # self.articles_by_user_id = generate_loader_by_foreign_key(ArticleType, 'creator_id')
        self.articles_by_user_id = ArticlesByUserIdLoader()
        self.article_count_by_user_id = ArticleCountByUserIdLoader()


class DataLoaderMiddleware:

    def resolve(self, next, root, info, **kwargs):
        if not hasattr(info.context, 'loaders'):
            info.context.loaders = DataLoaders()

        return next(root, info, **kwargs)
