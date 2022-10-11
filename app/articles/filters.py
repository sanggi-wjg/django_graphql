import copy

import django_filters
from django_filters.filterset import FilterSetMetaclass, BaseFilterSet

from app.articles.models import Article, Comment
from app.authentication.models import User


class CustomBaseFilterSet(BaseFilterSet):

    def __init__(self, data=None, queryset=None, *, request=None, prefix=None):
        if queryset is None:
            queryset = self._meta.model._default_manager.all()
        if not hasattr(queryset, 'model'):
            model = self._meta.model
        else:
            model = queryset.model

        self.is_bound = data is not None
        self.data = data or {}
        self.queryset = queryset
        self.request = request
        self.form_prefix = prefix

        self.filters = copy.deepcopy(self.base_filters)

        # propagate the model and filterset to the filters
        for filter_ in self.filters.values():
            filter_.model = model
            filter_.parent = self

    @property
    def qs(self):
        if not hasattr(self, '_qs'):
            qs = self.queryset
            if self.is_bound:
                # ensure form validation before filtering
                self.errors
                qs = self.filter_queryset(qs)
            self._qs = qs
        return self._qs


class CustomFilterSet(CustomBaseFilterSet, metaclass=FilterSetMetaclass):
    pass


# class ArticleFilter(django_filters.FilterSet):
class ArticleFilter(CustomFilterSet):
    class Meta:
        model = Article
        fields = (
            "slug", "title", "content", "creator", "creator__username"
        )
        ordering = ('-datetime_created', '-datetime_updated')

    slug = django_filters.CharFilter(lookup_expr='exact')
    title = django_filters.CharFilter(lookup_expr='contains')
    content = django_filters.CharFilter(lookup_expr='contains')
    creator = django_filters.ModelChoiceFilter(queryset=User.objects.filter(is_active=True).all())
    creator__username = django_filters.CharFilter(lookup_expr='exact')

    order_by = django_filters.OrderingFilter(
        fields=(
            ('datetime_created', 'datetime_updated', 'title', 'content')
        )
    )


class CommentFilter(django_filters.FilterSet):
    class Meta:
        model = Comment
        fields = (
            "content", "creator", "datetime_created", "datetime_updated"
        )

    article = django_filters.ModelChoiceFilter(queryset=Article.objects.filter().all())
