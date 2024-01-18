import requests as rq
import pandas as pd
import numpy as np
import datetime as dt
import statistics as st
import os
from dotenv import load_dotenv

from django.core.paginator import Paginator

from .models import Sku, ExcBrands, ExcNaming

load_dotenv()

# Токен из кабинета WB
TOKEN = os.getenv('WB_TOKEN')
# Базовый URL API WB
URL = 'https://mpstats.io/api/wb/get/'
# Хидеры для подключения к API и получения нужного формата данных
HEADERS = {
    'X-Mpstats-TOKEN': TOKEN,
    'Content-Type': 'application/json'
}

SKU_FIRST_DATE = 30

# Получаем все нужные нам даты 
today = dt.datetime.today().date()
sku_first_date = (today - dt.timedelta(days=SKU_FIRST_DATE+1)).strftime(
    '%Y-%m-%d'
)
yesterday = (today - dt.timedelta(days=1)).strftime('%Y.%m.%d')
two_weeks = (today - dt.timedelta(days=15)).strftime('%Y.%m.%d')
three_weeks = (today - dt.timedelta(days=22)).strftime('%Y.%m.%d')
month_ago = (today - dt.timedelta(days=31)).strftime('%Y.%m.%d')


def get_page_obj(obj_list, request):
    paginator = Paginator(obj_list, 30)
    page_number = request.GET.get('page')
    if not page_number:
        page_number = request.session.get('page')
    page_object = paginator.get_page(page_number)
    return page_object


def get_all_items(cat):
    dates_range = f'd1={yesterday}&{month_ago}'
    new_url = f'{URL}subject?{dates_range}&path={cat.id_wb}'
    payload = {
        'startRow': 0,
        'endRow': 5000,
        'filterModel': {
                        'days_with_sales':
                        {  # Фильтр по количеству дней с продажами
                            'filterType': 'number',
                            'type': 'greaterThanOrEqual',
                            'filter': 3
                        },
                        'sku_first_date':
                        {  # Поставим фильтр по SKU_first_date
                            'dateFrom': f'{sku_first_date} 00:00:00',
                            'dateTo': 'null',
                            'filterType': 'date',
                            'type': 'greaterThan'
                        },
                        'sales':
                        {  # Фильтр по количеству продаж
                            'filterType': 'number',
                            'type': 'greaterThanOrEqual',
                            'filter': cat.min_total_sells
                        }
                        },
        'sortModel': [{'colId': 'revenue', 'sort': 'desc'}]
    }
    query = rq.post(new_url, headers=HEADERS, json=payload).json()
    work_df = pd.DataFrame(query['data'])
    return (work_df.to_dict('records'))


def update_db(cat):
    '''Функция для обновления БД.'''
    # Получаем всю выгрузку по категории
    items = get_all_items(cat)
    banned_brands = ExcBrands.objects.all()
    bb_list = [x.brand.lower() for x in banned_brands]
    banned_words = ExcNaming.objects.all()
    bw_list = [x.word.lower() for x in banned_words]
    model_instances = []
    print(items[0])
    for record in items:
        # Получаем графики цен для 4-х временных промежутков
        if record['brand'].lower() in bb_list:
            continue
        skip = False
        for word in bw_list:
            if word.lower() in record['name'].lower():
                skip = True
                break
        if skip:
            continue
        price_graph = record['price_graph']
        price_lists = [
            price_graph[-8::],
            price_graph[-14::],
            price_graph[-21::],
            price_graph,
        ]
        median_price = [0, 0, 0, 0]
        i = 0
        # Прогоняем цикл для подсчета медианных цен
        for p_l in price_lists:
            if (check_price_list(p_l)):
                p_l_ex = [float(x) for x in p_l if x != 0]
                median_price[i] = st.median(p_l_ex)
            else:
                median_price[i] = 0
            i += 1
        # Если хотя бы для одного промежутка выполняется условие
        # То продолжаем обрабатывать товар
        if not check_medians(median_price, cat):
            continue
        # Получаем графики продаж для 4-х временных промежутков
        sells_graph = record['graph']
        sells_lists = [
            sells_graph[-8::],
            sells_graph[-14::],
            sells_graph[-21::],
            sells_graph,
        ]
        min_avg_flags = [False, False, False, False]
        fix_avg_flags = [False, False, False, False]
        sells_growth_flags = [False, False, False, False]
        i = 0
        # Прогоняем цикл для проверки выполнения условий по продажам
        for s_l in sells_lists:
            min_avg_flags[i] = check_min_avg_sells(s_l, cat.min_sells)
            fix_avg_flags[i] = check_fix_avg(
                s_l, price_lists[i], median_price[i], cat.fix_avg_sells
            )
            sells_growth_flags[i] = check_avg_sales_growth(
                s_l, price_lists[i], median_price[i]
            )
            i += 1
        # Если хотя бы для одного промежутка выполняется условие
        # То продолжаем обрабатывать товар
        if not any(min_avg_flags):
            continue
        # Получаем графики остатков для 4-х временных промежутков
        stocks_graph = record['stocks_graph']
        stocks_lists = [
            stocks_graph[-8::],
            stocks_graph[-14::],
            stocks_graph[-21::],
            stocks_graph,
        ]
        stocks_flags = [False, False, False, False]
        i = 0
        # Прогоняем цикл для проверки выполнения условий по остаткам
        for s_l in stocks_lists:
            stocks_flags[i] = check_stocks(s_l)
            i += 1
        # Если хотя бы для одного промежутка выполняется условие
        # То продолжаем обрабатывать товар
        comb_flags = []
        
        for i in range(4):
            comb_flags.append(
                min_avg_flags[i] and (stocks_flags[i]
                                      or fix_avg_flags[i]
                                      or sells_growth_flags[i])
            )
        if not any(comb_flags):
            continue
        # Если дошли до сюда, то можно сохранять товар в базу
        model_instances.append(
            Sku(
                sku_id=record['id'],
                name=record['name'],
                brand=record['brand'],
                thumb_middle=record['thumb_middle'],
                sku_first_date=dt.datetime.strptime(
                    record['sku_first_date'], '%Y-%m-%d'
                ),
                median_price8=median_price[0],
                median_price14=median_price[1],
                median_price21=median_price[2],
                median_price30=median_price[3],
                sells_graph8=','.join(str(x) for x in sells_lists[0]),
                sells_graph14=','.join(str(x) for x in sells_lists[1]),
                sells_graph21=','.join(str(x) for x in sells_lists[2]),
                sells_graph30=','.join(str(x) for x in sells_lists[3]),
                stocks_graph8=','.join(str(x) for x in stocks_lists[0]),
                stocks_graph14=','.join(str(x) for x in stocks_lists[1]),
                stocks_graph21=','.join(str(x) for x in stocks_lists[2]),
                stocks_graph30=','.join(str(x) for x in stocks_lists[3]),
                min_avg_sells8=min_avg_flags[0],
                min_avg_sells14=min_avg_flags[1],
                min_avg_sells21=min_avg_flags[2],
                min_avg_sells30=min_avg_flags[3],
                fix_avg_8=fix_avg_flags[0],
                fix_avg_14=fix_avg_flags[1],
                fix_avg_21=fix_avg_flags[2],
                fix_avg_30=fix_avg_flags[3],
                avg_sells_growth8=sells_growth_flags[0],
                avg_sells_growth14=sells_growth_flags[1],
                avg_sells_growth21=sells_growth_flags[2],
                avg_sells_growth30=sells_growth_flags[3],
                stocks8=stocks_flags[0],
                stocks14=stocks_flags[1],
                stocks21=stocks_flags[2],
                stocks30=stocks_flags[3],
                sells_stocks8=comb_flags[0],
                sells_stocks14=comb_flags[1],
                sells_stocks21=comb_flags[2],
                sells_stocks30=comb_flags[3],
                category=cat,
                revenue=record['revenue'],
                gender=record['gender'],
                turnover_days=record['turnover_days']
            )
        )
    Sku.objects.bulk_create(model_instances)


def check_price_list(price_list):
    price_list = [float(x) for x in price_list if x != 0]
    if len(price_list) == 0:
        return False
    return True


def check_medians(medians, cat):
    for x in medians:
        if ((x >= cat.min_price) or
           (x <= cat.max_price)):
            return True
    return False


def check_avg_sales_growth(item_sells_graph, price_graph, med_price):
    ''' Проверка на рост средних продаж.'''
    check_zeros = 0
    # Проверяем, не все ли по нулям
    if sum(item_sells_graph) == 0:
        return False
    # Смотрим, если кол-во дней с продажами <5 то и проверять нечего
    for x in item_sells_graph:
        if x > 0:
            check_zeros += 1
    if check_zeros < 5:
        return False
    # Ищем первый день, когда появились продажи
    start = 0
    for x in range(len(item_sells_graph)):
        if item_sells_graph[x] != 0:
            start = x
            break
    list_wo_z = item_sells_graph[start::]
    price_g_new = price_graph[start::]
    # Рассчитываем СКО + предельные отклонения
    std_metric = np.std(list_wo_z)
    boost = st.mean(list_wo_z) + 2 * std_metric
    drop = st.mean(list_wo_z) - 2 * std_metric
    # Рассчитаем среднее первых 4-х дней
    count = 0
    sum_l = 0
    avg_first_4 = 0
    x = 0
    while x < len(list_wo_z):
        if price_g_new[x] > 2 * med_price:
            x += 1
            continue
        if list_wo_z[x] < boost and list_wo_z[x] > drop:
            sum_l += list_wo_z[x]
            count += 1
        if count == 4:
            avg_first_4 = sum_l / count
        x += 1
    if count <= 4:
        return False
    elif sum_l / count > avg_first_4:
        return True
    return False


def check_fix_avg(item_sells_graph, price_graph, med_price, avg_fix):
    ''' Проверка на фикс средние продажи.'''
    # Проверяем, не все ли по нулям
    if sum(item_sells_graph) == 0:
        return False
    start = 0
    for x in range(len(item_sells_graph)):
        if item_sells_graph[x] != 0:
            start = x
            break
    list_wo_z = item_sells_graph[start::]
    price_g_new = price_graph[start::]
    # Рассчитываем СКО + предельные отклонения
    std_metric = np.std(list_wo_z)
    boost = st.mean(list_wo_z) + 2 * std_metric
    drop = st.mean(list_wo_z) - 2 * std_metric
    count = 0
    sum_l = 0
    x = 0
    while x < len(list_wo_z):
        if price_g_new[x] > 2 * med_price:
            x += 1
            continue
        if list_wo_z[x] < boost and list_wo_z[x] > drop:
            sum_l += list_wo_z[x]
            count += 1
        x += 1
    if count == 0:
        return False
    if sum_l / count >= avg_fix:
        return True
    return False


def check_stocks_rev(stocks_graph):
    '''Проверка на высохшие остатки c конца.'''
    start_stocks = -1
    for x in range(len(stocks_graph)):
        if stocks_graph[x] != 0:
            start_stocks = stocks_graph[x]
            break
    if start_stocks == -1:
        return False
    rev_list = stocks_graph[::-1]
    x = 1
    while x < len(rev_list):
        if rev_list[x-1] <= rev_list[x]:
            x += 1
            continue
        else:
            if (rev_list[x] <= 1.3 * rev_list[x-1]
               and rev_list[0] <= 0.3 * rev_list[x-1]):
                return True
        x += 1
    return False


def check_stocks(stocks_graph):
    '''Проверка на высохшие остатки c начала.'''
    start = 0
    start_stocks = -1
    for x in range(len(stocks_graph)):
        if stocks_graph[x] != 0:
            start_stocks = stocks_graph[x]
            start = x
            break
    if start_stocks == -1:
        return False
    prev = start_stocks
    while start < len(stocks_graph):
        if stocks_graph[start] <= 0.3 * start_stocks:
            return True
        elif stocks_graph[start] >= 1.3 * prev:
            start_stocks = stocks_graph[start]
        prev = stocks_graph[start]
        start += 1
    return False


def check_min_avg_sells(item_sells_graph, min_avg_bench):
    '''Первичная проверка на средние продажи'''
    if sum(item_sells_graph) == 0:
        return False
    for x in range(len(item_sells_graph)):
        if item_sells_graph[x] != 0:
            start = x
            break
    avg = st.mean(item_sells_graph[start::])
    if avg >= min_avg_bench:
        return True
    return False
