import django_filters
from django.contrib.auth.models import User

from app.articles.models import Article


class ArticleFilter(django_filters.FilterSet):
    class Meta:
        model = Article
        fields = (
            "slug", "title", "content", "creator", "creator__username"
        )
        # ordering = ('-datetime_created', '-datetime_updated')

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
    # default_order = ('-datetime_created', '-datetime_updated')

    @property
    def qs(self):
        return super(ArticleFilter, self).qs.filter()
