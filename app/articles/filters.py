import django_filters

from app.articles.models import Article, Comment
from app.authentication.models import User


class ArticleFilter(django_filters.FilterSet):
    class Meta:
        model = Article
        fields = (
            "slug", "title", "content", "creator", "creator__username"
        )
        # ordering = ('-datetime_created', '-datetime_updated')

    slug = django_filters.CharFilter(lookup_expr='exact')
    title = django_filters.CharFilter(lookup_expr='exact')
    title_contains = django_filters.CharFilter(lookup_expr='contains')
    content = django_filters.CharFilter(lookup_expr='contains')
    creator = django_filters.ModelChoiceFilter(queryset=User.objects.filter(is_active=True).all())
    creator__username = django_filters.CharFilter(lookup_expr='exact')

    order_by = django_filters.OrderingFilter(
        fields=(
            ('datetime_created', 'datetime_updated', 'title', 'content')
        )
    )

    @property
    def qs(self):
        return super(ArticleFilter, self).qs.filter()


class CommentFilter(django_filters.FilterSet):
    class Meta:
        model = Comment
        fields = (
            "content", "creator", "datetime_created", "datetime_updated"
        )

    article = django_filters.ModelChoiceFilter(queryset=Article.objects.filter().all())
