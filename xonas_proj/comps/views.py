import datetime as dt

from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.http import HttpResponseRedirect

from .models import Category, Favorites, Sku
from .utils import (get_page_obj,
                    update_db,
                    today,
                    )


@login_required
def cats(request):
    template = 'comps/cats.html'
    categories = Category.objects.all()
    context = {'category_list': categories}
    return render(request, template, context)


@login_required
def cat_list8(request, category_slug):
    dt_check = Sku.objects.all().first()
    if not dt_check or dt_check.created_at.date() != today:
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
    date_from = (today - dt.timedelta(days=8))
    items_list = Sku.objects.select_related(
        'category'
    ).filter(
        category=chosen_category,
        sku_first_date__gte=date_from,
        median_price8__gte=chosen_category.min_price,
        median_price8__lte=chosen_category.max_price,
        boost8=True,
        sells_stocks8=True
        ).annotate(
            sells_list=F('sells_graph8'),
            stocks_list=F('stocks_graph8'),
            median_price=F('median_price8'),
            avg_sells=F('avg_sells8'),
            stocks=F('stocks8'),
    )
    likes_list = Favorites.objects.filter(
        user=request.user,
        fav__category=chosen_category,
    )
    likes = [x.fav for x in likes_list]
    dts = [
        (today - dt.timedelta(days=x + 1)).strftime('%d') for x in range(8)
    ][::-1]
    context = {
        'page_obj': get_page_obj(items_list, request),
        'dts': dts,
        'likes': likes,
    }
    return render(request, template, context)


@login_required
def cat_list14(request, category_slug):
    dt_check = Sku.objects.all().first()
    if not dt_check or dt_check.created_at.date() != today:
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
    date_from = (today - dt.timedelta(days=14))
    items_list = Sku.objects.select_related(
        'category'
    ).filter(
        category=chosen_category,
        sku_first_date__gte=date_from,
        median_price14__gte=chosen_category.min_price,
        median_price14__lte=chosen_category.max_price,
        boost14=True,
        sells_stocks14=True
        ).annotate(
            sells_list=F('sells_graph14'),
            stocks_list=F('stocks_graph14'),
            median_price=F('median_price14'),
            avg_sells=F('avg_sells14'),
            stocks=F('stocks14'),
    )
    likes_list = Favorites.objects.filter(
        user=request.user,
        fav__category=chosen_category,
    )
    likes = [x.fav for x in likes_list]
    dts = [
        (today - dt.timedelta(days=x + 1)).strftime('%d') for x in range(14)
    ][::-1]
    context = {
        'page_obj': get_page_obj(items_list, request),
        'dts': dts,
        'likes': likes,
    }
    return render(request, template, context)


@login_required
def cat_list21(request, category_slug):
    dt_check = Sku.objects.all().first()
    if not dt_check or dt_check.created_at.date() != today:
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
    date_from = (today - dt.timedelta(days=21))
    items_list = Sku.objects.select_related(
        'category'
    ).filter(
        category=chosen_category,
        sku_first_date__gte=date_from,
        median_price21__gte=chosen_category.min_price,
        median_price21__lte=chosen_category.max_price,
        boost21=True,
        sells_stocks21=True
        ).annotate(
            sells_list=F('sells_graph21'),
            stocks_list=F('stocks_graph21'),
            median_price=F('median_price21'),
            avg_sells=F('avg_sells21'),
            stocks=F('stocks21'),
    )
    likes_list = Favorites.objects.filter(
        user=request.user,
        fav__category=chosen_category,
    )
    likes = [x.fav for x in likes_list]
    dts = [
        (today - dt.timedelta(days=x + 1)).strftime('%d') for x in range(21)
    ][::-1]
    context = {
        'page_obj': get_page_obj(items_list, request),
        'dts': dts,
        'likes': likes,
    }
    return render(request, template, context)


@login_required
def cat_list30(request, category_slug):
    dt_check = Sku.objects.all().first()
    if not dt_check or dt_check.created_at.date() != today:
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
    date_from = (today - dt.timedelta(days=30))
    items_list = Sku.objects.select_related(
        'category'
    ).filter(
        category=chosen_category,
        sku_first_date__gte=date_from,
        median_price30__gte=chosen_category.min_price,
        median_price30__lte=chosen_category.max_price,
        boost30=True,
        sells_stocks30=True
        ).annotate(
            sells_list=F('sells_graph30'),
            stocks_list=F('stocks_graph30'),
            median_price=F('median_price30'),
            avg_sells=F('avg_sells30'),
            stocks=F('stocks30'),
    )
    likes_list = Favorites.objects.filter(
        user=request.user,
        fav__category=chosen_category,
    )
    likes = [x.fav for x in likes_list]
    dts = [
        (today - dt.timedelta(days=x + 1)).strftime('%d') for x in range(30)
    ][::-1]
    context = {
        'page_obj': get_page_obj(items_list, request),
        'dts': dts,
        'likes': likes,
    }
    return render(request, template, context)


@login_required
def like_item(request):
    sku_id = request.GET.get('id')
    sku = get_object_or_404(Sku, pk=sku_id)
    user = request.user
    new_like = Favorites(
        user=user,
        fav=sku,
    )
    new_like.save(force_insert=True)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def favorites(request):
    favs = Favorites.objects.filter(
        user=request.user
    ).select_related('fav')
    cats = [x.fav.category.name for x in favs]
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