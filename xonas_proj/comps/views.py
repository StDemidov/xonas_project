import datetime as dt
import statistics as st
from django.shortcuts import get_object_or_404, render, redirect

from .models import Category, Sku
from .utils import get_page_obj, update_db, today


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
    stat_dict = dict()
    days = int(request.GET.get('days'))
    for item in items_list:
        price_list = item.price_graph.split(',')[-days::]
        price_list = [float(x) for x in price_list if x != '0']
        sells_list = item.sells_graph.split(',')[-days::]
        sells_list = [int(x) for x in sells_list]
        stocks_list = item.stocks_graph.split(',')[-days::]
        stocks_list = [int(x) for x in sells_list]
        if len(price_list) == 0:
            median_price = 0
        else:
            median_price = st.median(price_list)
        stat_dict[item.sku_id] = {}
        stat_dict[item.sku_id]['sells_list'] = sells_list
        stat_dict[item.sku_id]['stocks_list'] = stocks_list
        stat_dict[item.sku_id]['median_price'] = median_price
    context = {
        'page_obj': get_page_obj(items_list, request),
        'sku_dict': stat_dict,
        'days': days,
        }
    return render(request, template, context)
