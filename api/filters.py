import django_filters

from store.models import Product


class ProductFilter(django_filters.FilterSet):

    min_price = django_filters.NumberFilter(lookup_expr='gte', field_name='price')
    max_price = django_filters.NumberFilter(lookup_expr='lte', field_name='price')

    class Meta:
        model = Product
        fields = [
            'category',
            'tags',
            'user',
            'receive_type',
            'rating',
            'is_published',
        ]