import requests as rq
import pandas as pd
import datetime as dt
import os
from dotenv import load_dotenv

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

T_SHIRT_ID = '192'
TOP_ID = '185'
PANTS_ID = '11'
HOODIE_ID = '1724'
SWEAT_ID = '159'
LONG_ID = '217'
SHORTS_ID = '151'
JACKETS_ID = '168'

SKU_FIRST_DATE = 8 # Это можно менять, ставим количество дней назад, с какой даты обнаруживать новинки
TOTAL_SALES = 8 # Это можно менять

# Получаем все нужные нам даты 
today = dt.datetime.today().date()
yesterday = (today - dt.timedelta(days=1)).strftime('%Y.%m.%d')
sku_first_date = (today - dt.timedelta(days=SKU_FIRST_DATE+1)).strftime('%Y-%m-%d')
month_ago = (today - dt.timedelta(days=30)).strftime('%Y.%m.%d')


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
                            'type': 'lessThan'
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
