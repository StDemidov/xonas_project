from .models import Sku
import django_filters


class SkuFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Sku
        fields = ['name']