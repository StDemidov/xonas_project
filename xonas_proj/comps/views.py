import datetime as dt

from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import F, Q
from django.http import HttpResponseRedirect

from .models import Category, Favorites, Sku
from .utils import (get_page_obj,
                    update_db,
                    today,
                    )
from .filters import Sku8Filter, Sku14Filter, Sku21Filter, Sku30Filter


@login_required
def force_upd(request):
    cats = Category.objects.all()
    instance = Sku.objects.all()
    instance.delete()
    for cat in cats:
        update_db(cat)
    return redirect('comps:cats')


@login_required
def cats(request):
    template = 'comps/cats.html'
    categories = Category.objects.all()
    context = {'category_list': categories}
    return render(request, template, context)


@login_required
def cat_list8(request, category_slug):
    template = 'comps/list.html'
    chosen_category = get_object_or_404(
        Category.objects.filter(
            slug=category_slug,
        ),
    )
    date_from = (today - dt.timedelta(days=8))
    items_list = Sku.objects.select_related(
        'category'
    ).filter(
        category=chosen_category,
        sku_first_date__gte=date_from,
        median_price8__gte=chosen_category.min_price,
        median_price8__lte=chosen_category.max_price,
        sells_stocks8=True
        ).filter(
            Q(avg_sells_growth8=True) | Q(fix_avg_8=True) | Q(stocks8=True)
        ).annotate(
            sells_list=F('sells_graph8'),
            stocks_list=F('stocks_graph8'),
            median_price=F('median_price8'),
            fix_avg=F('fix_avg_8'),
            avg_sells_growth=F('avg_sells_growth8'),
            stocks=F('stocks8'),
    )
    sku_filter = Sku8Filter(request.GET, queryset=items_list)
    items_list = sku_filter.qs
    likes_list = Favorites.objects.filter(
        user=request.user,
        category=chosen_category,
    )
    likes = [x.sku_id for x in likes_list]
    dts = [
        (today - dt.timedelta(days=x + 1)).strftime('%d') for x in range(8)
    ][::-1]
    context = {
        'page_obj': get_page_obj(items_list, request),
        'dts': dts,
        'likes': likes,
        'myFilter': sku_filter
    }
    return render(request, template, context)


@login_required
def cat_list14(request, category_slug):
    template = 'comps/list.html'
    chosen_category = get_object_or_404(
        Category.objects.filter(
            slug=category_slug,
        ),
    )
    date_from = (today - dt.timedelta(days=14))
    items_list = Sku.objects.select_related(
        'category'
    ).filter(
        category=chosen_category,
        sku_first_date__gte=date_from,
        median_price14__gte=chosen_category.min_price,
        median_price14__lte=chosen_category.max_price,
        sells_stocks14=True
        ).filter(
            Q(avg_sells_growth14=True) | Q(fix_avg_14=True) | Q(stocks14=True)
        ).annotate(
            sells_list=F('sells_graph14'),
            stocks_list=F('stocks_graph14'),
            median_price=F('median_price14'),
            fix_avg=F('fix_avg_14'),
            avg_sells_growth=F('avg_sells_growth14'),
            stocks=F('stocks14'),
        )
    sku_filter = Sku14Filter(request.GET, queryset=items_list)
    items_list = sku_filter.qs
    likes_list = Favorites.objects.filter(
        user=request.user,
        category=chosen_category,
    )
    likes = [x.sku_id for x in likes_list]
    dts = [
        (today - dt.timedelta(days=x + 1)).strftime('%d') for x in range(14)
    ][::-1]
    context = {
        'page_obj': get_page_obj(items_list, request),
        'dts': dts,
        'likes': likes,
        'myFilter': sku_filter
    }
    return render(request, template, context)


@login_required
def cat_list21(request, category_slug):
    template = 'comps/list.html'
    chosen_category = get_object_or_404(
        Category.objects.filter(
            slug=category_slug,
        ),
    )
    date_from = (today - dt.timedelta(days=21))
    items_list = Sku.objects.select_related(
        'category'
    ).filter(
        category=chosen_category,
        sku_first_date__gte=date_from,
        median_price21__gte=chosen_category.min_price,
        median_price21__lte=chosen_category.max_price,
        sells_stocks21=True
        ).filter(
            Q(avg_sells_growth21=True) | Q(fix_avg_21=True) | Q(stocks21=True)
        ).annotate(
            sells_list=F('sells_graph21'),
            stocks_list=F('stocks_graph21'),
            median_price=F('median_price21'),
            fix_avg=F('fix_avg_21'),
            avg_sells_growth=F('avg_sells_growth21'),
            stocks=F('stocks21'),
            )
    sku_filter = Sku21Filter(request.GET, queryset=items_list)
    items_list = sku_filter.qs  
    likes_list = Favorites.objects.filter(
        user=request.user,
        category=chosen_category,
    )
    likes = [x.sku_id for x in likes_list]
    dts = [
        (today - dt.timedelta(days=x + 1)).strftime('%d') for x in range(21)
    ][::-1]
    context = {
        'page_obj': get_page_obj(items_list, request),
        'dts': dts,
        'likes': likes,
        'myFilter': sku_filter
    }
    return render(request, template, context)


@login_required
def cat_list30(request, category_slug):
    template = 'comps/list.html'
    chosen_category = get_object_or_404(
        Category.objects.filter(
            slug=category_slug,
        ),
    )
    date_from = (today - dt.timedelta(days=30))
    items_list = Sku.objects.select_related(
        'category'
    ).filter(
        category=chosen_category,
        sku_first_date__gte=date_from,
        median_price30__gte=chosen_category.min_price,
        median_price30__lte=chosen_category.max_price,
        sells_stocks30=True,
        ).filter(
            Q(avg_sells_growth30=True) | Q(fix_avg_30=True) | Q(stocks30=True)
        ).annotate(
                sells_list=F('sells_graph30'),
                stocks_list=F('stocks_graph30'),
                median_price=F('median_price30'),
                fix_avg=F('fix_avg_30'),
                avg_sells_growth=F('avg_sells_growth30'),
                stocks=F('stocks30'),
        )
    sku_filter = Sku30Filter(request.GET, queryset=items_list)
    items_list = sku_filter.qs  
    likes_list = Favorites.objects.filter(
        user=request.user,
        category=chosen_category,
    )
    likes = [x.sku_id for x in likes_list]
    dts = [
        (today - dt.timedelta(days=x + 1)).strftime('%d') for x in range(30)
    ][::-1]
    context = {
        'page_obj': get_page_obj(items_list, request),
        'dts': dts,
        'likes': likes,
        'myFilter': sku_filter,

    }
    return render(request, template, context)


@login_required
def like_item(request):
    sku_id = request.GET.get('id')
    sku = get_object_or_404(Sku, pk=sku_id)
    user = request.user
    new_like = Favorites(
        user=user,
        sku_id=sku.sku_id,
        name=sku.name,
        brand=sku.brand,
        thumb_middle=sku.thumb_middle,
        sku_first_date=sku.sku_first_date,
        category=sku.category,
    )
    new_like.save(force_insert=True)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def favorites(request):
    favs = Favorites.objects.filter(
        user=request.user
    )
    cats = [x.category.name for x in favs]
    cats = set(cats)
    template = 'comps/favorites.html'
    context = {
        'favs': favs,
        'cats': cats
    }
    return render(request, template, context)


@login_required
def del_item(request, id):
    instance = Favorites.objects.filter(
        user=request.user,
        id=id
    )
    if instance.exists():
        instance.delete()
    return redirect('comps:favorites')