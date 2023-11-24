import requests as rq
import pandas as pd
import datetime as dt
import statistics as st
import os
from dotenv import load_dotenv

from django.core.paginator import Paginator

from .models import Sku

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
TOTAL_SALES = 20

# Получаем все нужные нам даты 
today = dt.datetime.today().date()
sku_first_date = (today - dt.timedelta(days=SKU_FIRST_DATE+1)).strftime('%Y-%m-%d')
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
        'filterModel': {'final_price':
                        {  # Фильтр по последней цене
                            'filterType': 'number',
                            'type': 'inRange',
                            'filter': int(cat.min_price),
                            'filterTo': int(cat.max_price)
                        },
                        'days_with_sales':
                        {  # Фильтр по количеству дней с продажами
                            'filterType': 'number',
                            'type': 'greaterThanOrEqual',
                            'filter': 3
                        },
                        'sku_first_date':
                        {  # Чтоб получить только новинки поставим фильтр по SKU_first_date
                            'dateFrom': f'{sku_first_date} 00:00:00',
                            'dateTo': 'null',
                            'filterType': 'date',
                            'type': 'greaterThan'
                        },
                        'sales':
                        {  # Фильтр по количеству продаж
                            'filterType': 'number',
                            'type': 'greaterThanOrEqual',
                            'filter': TOTAL_SALES
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
    model_instances = []
    for record in items:
        # Получаем графики цен для 4-х временных промежутков
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
                p_l_ex = [float(x) for x in p_l if x != '0']
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
        sells_flags = [False, False, False, False]
        boost_flags = [False, False, False, False]
        i = 0
        # Прогоняем цикл для проверки выполнения условий по продажам
        for s_l in sells_lists:
            sells_flags[i] = check_avg_sales(s_l, cat.min_sells)
            boost_flags[i] = check_sales_boost(s_l)
            i += 1
        # Если хотя бы для одного промежутка выполняется условие
        # То продолжаем обрабатывать товар
        if not any(boost_flags):
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
        if not any(sells_flags) and not any(stocks_flags):
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
                boost8=boost_flags[0],
                boost14=boost_flags[1],
                boost21=boost_flags[2],
                boost30=boost_flags[3],
                avg_sells8=sells_flags[0],
                avg_sells14=sells_flags[1],
                avg_sells21=sells_flags[2],
                avg_sells30=sells_flags[3],
                stocks8=stocks_flags[0],
                stocks14=stocks_flags[1],
                stocks21=stocks_flags[2],
                stocks30=stocks_flags[3],
                sells_stocks8=stocks_flags[0] or sells_flags[0],
                sells_stocks14=stocks_flags[0] or sells_flags[0],
                sells_stocks21=stocks_flags[0] or sells_flags[0],
                sells_stocks30=stocks_flags[0] or sells_flags[0],
                category=cat
            )
        )
    Sku.objects.bulk_create(model_instances)


def check_price_list(price_list):
    price_list = [float(x) for x in price_list if x != '0']
    if len(price_list) == 0:
        return False
    return True


def check_medians(medians, cat):
    for x in medians:
        if ((x >= cat.min_price) or
           (x <= cat.max_price)):
            return True
    return False


def check_sales_boost(item_sells_graph):
    prev = 0
    for x in item_sells_graph:
        if x == 0:
            continue
        else:
            prev = x
            break
    for x in item_sells_graph:
        if x != 0:
            if x >= prev * 5:
                return False
            prev = x
    return True


def check_avg_sales(item_sells_graph, avg_bench):
    ''' Проверка: кол-во продаж не 0, есть три дня с
    продажами, не больше 2-х дней с продажами ни ниже
    среднего.'''
    check_zeros = 0
    if sum(item_sells_graph) == 0:
        return False
    for x in item_sells_graph:
        if x > 0:
            check_zeros += 1
    if check_zeros < 3:
        return False
    below_avg_c = 0
    start = 0
    for x in range(len(item_sells_graph)):
        if item_sells_graph[x] != 0:
            start = x
    while start < len(item_sells_graph):
        if item_sells_graph[start] < avg_bench:
            below_avg_c += 1
        if below_avg_c == 3:
            return False
        start += 1
    return True


def check_stocks(stocks_graph):
    start = 0
    start_stocks = -1
    for x in range(len(stocks_graph)):
        if stocks_graph[x] != 0:
            start = x
            start_stocks = stocks_graph[start]
    if start_stocks == -1:
        return False
    while start < len(stocks_graph):
        if stocks_graph[start] <= 0.3 * start_stocks:
            return True
        start += 1
    return False
