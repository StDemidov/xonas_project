import datetime as dt
from django.shortcuts import get_object_or_404, render, redirect

from .models import Category, Sku
from .parse import get_all_items, today


def cats(request):
    template = 'comps/cats.html'
    categories = Category.objects.all()
    context = {'category_list': categories}
    return render(request, template, context)


def cat_list(request, category_slug):
    dt_check = Sku.objects.all().first()
    if dt_check.created_at.date() != today:
        cats = Category.objects.all()
        instance = Sku.objects.all()
        instance.delete()
        for cat in cats:
            update_db(cat)    
    template = 'comps/list.html'
    chosen_category = get_object_or_404(
        Category.objects.filter(
            slug=category_slug,
        ),
    )
    items_list = Sku.objects.select_related(
        'category'
    ).filter(category=chosen_category)
    context = {'items_list': items_list[:20]}
    return render(request, template, context)


def update_db(cat):
    items = get_all_items(cat)
    print(items)
    model_instances = [Sku(
        sku_id=record['id'],
        name=record['name'],
        brand=record['brand'],
        thumb=record['thumb'],
        thumb_middle=record['thumb_middle'],
        price_graph=','.join(str(x) for x in record['price_graph']),
        sells_graph=','.join(str(x) for x in record['graph']),
        stocks_graph=','.join(str(x) for x in record['stocks_graph']),
        sku_first_date=dt.datetime.strptime(record['sku_first_date'], '%Y-%m-%d'),
        category=cat,
    ) for record in items]
    Sku.objects.bulk_create(model_instances)
