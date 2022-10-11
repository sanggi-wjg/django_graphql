# from graphql import ResolveInfo
#
# from app.articles.types import ArticleType, UserType
# from app.core import base_loaders
#
#
# class SentryMiddleware(object):
#     """
#     Properly capture errors during query execution and send them to Sentry
#     Then raise the error again and let Graphene handle it
#     """
#
#     def on_error(self, error):
#         # capture_exception(error)
#         raise error
#
#     def resolve(self, next, root, info: ResolveInfo, **args):
#         """
#         This will run on every single GraphQL field.
#
#         You can think of each field in a GraphQL query as a function or method of the previous type which returns the next type.
#         In fact, this is exactly how GraphQL works.
#         Each field on each type is backed by a function called the resolver which is provided by the GraphQL server developer.
#         When a field is executed, the corresponding resolver is called to produce the next value.
#
#         Reference: https://graphql.org/learn/execution/
#         """
#         return next(root, info, **args).catch(self.on_error)
#
#
# from app.articles import loaders
# from app.articles.types import UserType, ArticleType
#
#
# class Loaders:
#
#     def __init__(self):
#         self.user_by_article = loaders.generate_loader(UserType, "id")
#         self.articles_by_user_loader = loaders.generate_loader_by_foreign_key(ArticleType, 'creator_id')
#
#
# class LoaderMiddleware:
#
#     def resolve(self, next, root, info, **kwargs):
#         if not hasattr(info.context, 'loaders'):
#             info.context.loaders = Loaders()
#
#         return next(root, info, **kwargs)
from collections import defaultdict

from django.db.models import Count
from promise import Promise
from promise.dataloader import DataLoader

from app.articles.models import Article


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
        article_counts = Article.objects.values('creator_id').filter(creator_id__in=user_ids).annotate(count=Count('creator_id'))

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
