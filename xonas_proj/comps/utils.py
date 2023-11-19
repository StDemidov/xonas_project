import requests as rq
import pandas as pd
import datetime as dt
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
    items = get_all_items(cat)
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
    for x in range(len(stocks_graph)):
        if stocks_graph[x] != 0:
            start = x
            start_stocks = stocks_graph[start]
    while start < len(stocks_graph):
        if stocks_graph[start] <= 0.3 * start_stocks:
            return True
        start += 1
    return False
