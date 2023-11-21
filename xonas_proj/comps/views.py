import datetime as dt
import statistics as st

from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required

from .models import Category, Favorites, Sku
from .utils import (get_page_obj,
                    update_db,
                    today,
                    check_sales_boost,
                    check_avg_sales,
                    check_stocks,
                    )


@login_required
def cats(request):
    template = 'comps/cats.html'
    categories = Category.objects.all()
    context = {'category_list': categories}
    return render(request, template, context)


@login_required
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
    try:
        days = int(request.GET.get('days'))
    except TypeError:
        days = int(request.session.get('days'))
    date_from = (today - dt.timedelta(days=days))
    items_list = Sku.objects.select_related(
        'category'
    ).filter(
        category=chosen_category,
        sku_first_date__gte=date_from)
    likes_list = Favorites.objects.filter(
        user=request.user,
        fav__category=chosen_category,
    )
    likes = [x.fav for x in likes_list]
    stat_dict = dict()
    list_to_exclude = []
    for item in items_list:
        price_list = item.price_graph.split(',')[-days::]
        price_list = [float(x) for x in price_list if x != '0']
        if len(price_list) == 0:
            list_to_exclude.append(item)
            continue
        else:
            median_price = st.median(price_list)
            if ((median_price < chosen_category.min_price) or
               (median_price > chosen_category.max_price)):
                list_to_exclude.append(item)
                continue
        sells_list = item.sells_graph.split(',')[-days::]
        sells_list = [int(x) for x in sells_list]
        stocks_list = item.stocks_graph.split(',')[-days::]
        stocks_list = [int(x) for x in stocks_list]  
        if ((not check_avg_sales(sells_list, chosen_category.min_sells)) and
           (not check_stocks(stocks_list))):
            list_to_exclude.append(item)
            continue
        if not check_sales_boost(sells_list):
            list_to_exclude.append(item)
            continue
        dts = [(today - dt.timedelta(days=x + 1)).strftime('%d') for x in range(days)]
        stat_dict[item.sku_id] = {}
        stat_dict[item.sku_id]['sells_list'] = sells_list
        stat_dict[item.sku_id]['stocks_list'] = stocks_list
        stat_dict[item.sku_id]['median_price'] = median_price
        stat_dict[item.sku_id]['avg_sales'] = check_avg_sales(
            sells_list, chosen_category.min_sells
        )
        stat_dict[item.sku_id]['stocks'] = check_stocks(stocks_list)
        stat_dict[item.sku_id]['dts'] = dts[::-1]
    res = items_list.exclude(id__in=[x.id for x in list_to_exclude])
    context = {
        'page_obj': get_page_obj(res, request),
        'sku_dict': stat_dict,
        'days': days,
        'likes': likes,
        }
    return render(request, template, context)


@login_required
def like_item(request, category_slug):
    sku_id = request.GET.get('id')
    sku = get_object_or_404(Sku, pk=sku_id)
    user = request.user
    new_like = Favorites(
        user=user,
        fav=sku,
    )
    new_like.save(force_insert=True)
    days = request.GET.get('days')
    page = request.GET.get('page')
    request.session['days'] = days
    request.session['page'] = page
    return redirect('comps:list', category_slug=category_slug)
