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
SKU_FIRST_DATE = 60 # Это можно менять, ставим количество дней назад, с какой даты обнаруживать новинки
TOTAL_SALES = 20 # Это можно менять

# Получаем все нужные нам даты 
today = dt.datetime.today().date()
yesterday = (today - dt.timedelta(days=1)).strftime('%Y.%m.%d')
two_weeks_ago = (today - dt.timedelta(days=14)).strftime('%Y.%m.%d')
sku_first_date = (today - dt.timedelta(days=SKU_FIRST_DATE+1)).strftime('%Y-%m-%d')


def get_t_shirts():
    dates_range = f'd1={yesterday}&{two_weeks_ago}'
    t_shirt_url = f'{URL}subject?{dates_range}&path=' + T_SHIRT_ID
    payload = {
        'startRow': 0,
        'endRow': 5000,
        'filterModel': {'final_price':
                        {  # Фильтр по последней цене
                            'filterType': 'number',
                            'type': 'inRange',
                            'filter': 1000,
                            'filterTo': 5000
                        },
                        'days_with_sales':
                        {  # Фильтр по количеству дней с продажами
                            'filterType': 'number',
                            'type': 'greaterThanOrEqual',
                            'filter': 10                     
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
    query = rq.post(t_shirt_url, headers=HEADERS, json=payload).json()
    work_df = pd.DataFrame(query['data'])
    return (work_df.to_dict('records'))
