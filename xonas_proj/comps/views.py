import datetime as dt

from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Count

from .models import Category, Sku
from .parse import get_t_shirts


def cats(request):
    template = 'comps/cats.html'
    categories = Category.objects.all().annotate(items_count=Count('skus'))
    context = {'category_list': categories}
    return render(request, template, context)


def cat_list(request, category_slug):
    template = 'comp/list.html'
    chosen_category = get_object_or_404(
        Category.objects.filter(
            slug=category_slug
        )
    )
    trends_list = Sku.objects.select_related(
        'category'
    ).filter(category=chosen_category)
    context = {'trends_list': trends_list}
    return render(request, template, context)


def update_db(request):
    instance = Sku.objects.all()
    instance.delete()
    t_shirts = get_t_shirts()
    categ = get_object_or_404(
        Category.objects.filter(
            slug='tshirt'
        )
    )
    model_instances = [Sku(
        sku_id=record['id'],
        name=record['name'],
        brand=record['brand'],
        thumb=record['thumb'],
        thumb_middle=record['thumb_middle'],
        price_graph=''.join(str(x) for x in record['price_graph']),
        sells_graph=''.join(str(x) for x in record['graph']),
        stocks_graph=''.join(str(x) for x in record['stocks_graph']),
        sku_first_date=dt.strptime(record['sku_first_date'], '%Y-%d-%m'),
        category=categ,
    ) for record in t_shirts]
    Sku.objects.bulk_create(model_instances)
    return redirect('comps:cats')
