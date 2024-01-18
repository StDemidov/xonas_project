import django_filters
from django import forms
from .models import Sku


class CustomBooleanFilter(django_filters.widgets.BooleanWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.choices = (('', ('Не важно')), ('true', ('Да')), ('false', ('Нет')))


class Sku8Filter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        field_name='name',
        lookup_expr='icontains',
        label='Название содержит',
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    name_exc = django_filters.CharFilter(
        field_name='name',
        lookup_expr='icontains',
        exclude=True,
        label='Исключить названия, которые содержат',
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )

    )
    turnover_days__gt = django_filters.NumberFilter(
        field_name='turnover_days',
        lookup_expr='gt',
        label='Оборачиваемость от (в днях):',
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "size": 40,
            }
        )
    )
    turnover_days__lt = django_filters.NumberFilter(
        field_name='turnover_days',
        lookup_expr='lt',
        label='Оборачиваемость до (в днях):',
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "size": 40,
            }
        )
    )
    median_price8__gt = django_filters.NumberFilter(
        field_name='median_price8',
        lookup_expr='gt',
        label='Цена от:',
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "size": 40,
            }
        )
    )
    median_price8__lt = django_filters.NumberFilter(
        field_name='median_price8',
        lookup_expr='lt',
        label='Цена до:',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    stocks8 = django_filters.BooleanFilter(
        field_name='stocks8',
        widget=CustomBooleanFilter(
            attrs={
                'class': 'form-select col',
            }
        ),
        label='Высыхание остатков',
    )
    avg_sells_growth8 = django_filters.BooleanFilter(
        field_name='avg_sells_growth8',
        widget=CustomBooleanFilter(
            attrs={
                'class': 'form-select col',
            }
        ),
        label='Рост. среднего'
    )
    fix_avg_8 = django_filters.BooleanFilter(
        field_name='fix_avg_8',
        widget=CustomBooleanFilter(
            attrs={
                'class': 'form-select col'
            }
        ),
        label='Фикс. среднее'
    )

    class Meta:
        model = Sku
        fields = []


class Sku14Filter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        field_name='name',
        lookup_expr='icontains',
        label='Название содержит',
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    name_exc = django_filters.CharFilter(
        field_name='name',
        lookup_expr='icontains',
        exclude=True,
        label='Исключить названия, которые содержат',
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )

    )
    turnover_days__gt = django_filters.NumberFilter(
        field_name='turnover_days',
        lookup_expr='gt',
        label='Оборачиваемость от (в днях):',
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "size": 40,
            }
        )
    )
    turnover_days__lt = django_filters.NumberFilter(
        field_name='turnover_days',
        lookup_expr='lt',
        label='Оборачиваемость до (в днях):',
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "size": 40,
            }
        )
    )
    median_price14__gt = django_filters.NumberFilter(
        field_name='median_price14',
        lookup_expr='gt',
        label='Цена от:',
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "size": 40,
            }
        )
    )
    median_price14__lt = django_filters.NumberFilter(
        field_name='median_price14',
        lookup_expr='lt',
        label='Цена до:',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    stocks14 = django_filters.BooleanFilter(
        field_name='stocks14',
        widget=CustomBooleanFilter(
            attrs={
                'class': 'form-select col',
            }
        ),
        label='Высыхание остатков',
    )
    avg_sells_growth14 = django_filters.BooleanFilter(
        field_name='avg_sells_growth14',
        widget=CustomBooleanFilter(
            attrs={
                'class': 'form-select col',
            }
        ),
        label='Рост. среднего'
    )
    fix_avg_14 = django_filters.BooleanFilter(
        field_name='fix_avg_14',
        widget=CustomBooleanFilter(
            attrs={
                'class': 'form-select col'
            }
        ),
        label='Фикс. среднее'
    )

    class Meta:
        model = Sku
        fields = []


class Sku21Filter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        field_name='name',
        lookup_expr='icontains',
        label='Название содержит',
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    name_exc = django_filters.CharFilter(
        field_name='name',
        lookup_expr='icontains',
        exclude=True,
        label='Исключить названия, которые содержат',
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )

    )
    turnover_days__gt = django_filters.NumberFilter(
        field_name='turnover_days',
        lookup_expr='gt',
        label='Оборачиваемость от (в днях):',
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "size": 40,
            }
        )
    )
    turnover_days__lt = django_filters.NumberFilter(
        field_name='turnover_days',
        lookup_expr='lt',
        label='Оборачиваемость до (в днях):',
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "size": 40,
            }
        )
    )
    median_price21__gt = django_filters.NumberFilter(
        field_name='median_price21',
        lookup_expr='gt',
        label='Цена от:',
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "size": 40,
            }
        )
    )
    median_price21__lt = django_filters.NumberFilter(
        field_name='median_price21',
        lookup_expr='lt',
        label='Цена до:',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    stocks21 = django_filters.BooleanFilter(
        field_name='stocks21',
        widget=CustomBooleanFilter(
            attrs={
                'class': 'form-select col',
            }
        ),
        label='Высыхание остатков',
    )
    avg_sells_growth21 = django_filters.BooleanFilter(
        field_name='avg_sells_growth21',
        widget=CustomBooleanFilter(
            attrs={
                'class': 'form-select col',
            }
        ),
        label='Рост. среднего'
    )
    fix_avg_21 = django_filters.BooleanFilter(
        field_name='fix_avg_21',
        widget=CustomBooleanFilter(
            attrs={
                'class': 'form-select col'
            }
        ),
        label='Фикс. среднее'
    )

    class Meta:
        model = Sku
        fields = []


class Sku30Filter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        field_name='name',
        lookup_expr='icontains',
        label='Название содержит',
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    name_exc = django_filters.CharFilter(
        field_name='name',
        lookup_expr='icontains',
        exclude=True,
        label='Исключить названия, которые содержат',
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )

    )
    turnover_days__gt = django_filters.NumberFilter(
        field_name='turnover_days',
        lookup_expr='gt',
        label='Оборачиваемость от (в днях):',
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "size": 40,
            }
        )
    )
    turnover_days__lt = django_filters.NumberFilter(
        field_name='turnover_days',
        lookup_expr='lt',
        label='Оборачиваемость до (в днях):',
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "size": 40,
            }
        )
    )
    median_price30__gt = django_filters.NumberFilter(
        field_name='median_price30',
        lookup_expr='gt',
        label='Цена от:',
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "size": 40,
            }
        )
    )
    median_price30__lt = django_filters.NumberFilter(
        field_name='median_price30',
        lookup_expr='lt',
        label='Цена до:',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    stocks30 = django_filters.BooleanFilter(
        field_name='stocks30',
        widget=CustomBooleanFilter(
            attrs={
                'class': 'form-select col',
            }
        ),
        label='Высыхание остатков',
    )
    avg_sells_growth30 = django_filters.BooleanFilter(
        field_name='avg_sells_growth30',
        widget=CustomBooleanFilter(
            attrs={
                'class': 'form-select col',
            }
        ),
        label='Рост. среднего'
    )
    fix_avg_30 = django_filters.BooleanFilter(
        field_name='fix_avg_30',
        widget=CustomBooleanFilter(
            attrs={
                'class': 'form-select col'
            }
        ),
        label='Фикс. среднее'
    )

    class Meta:
        model = Sku
        fields = []