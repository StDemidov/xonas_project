import requests as rq
import pandas as pd
import csv

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse

from .forms import ReportForm
from .utils import token_dict, REPORT_URL


@login_required
def reports(request):
    form = ReportForm
    template = 'reports/reports.html'
    context = {}
    if request.GET:
        form = ReportForm(request.GET)
        if form.is_valid():
            from_date = request.GET['from_date']
            to_date = request.GET['to_date']
            ip_token = token_dict[request.GET['ip']]
            headers = {'Authorization': ip_token}
            full_url = REPORT_URL + f'dateFrom={from_date}&dateTo={to_date}&rrdid=0&limit=100000'
            query = rq.get(full_url, headers=headers).json()
            df = pd.json_normalize(query)
            df = df.rename(
                columns={
                    'realizationreport_id': 'ID Отчета',
                    'date_from': 'Дата начала отчета',
                    'date_to': 'Дата конца отчета',
                    'create_dt': 'Дата создания отчета',
                    'currency_name': 'Валюта',
                    'suppliercontract_code': 'Код контракта',
                    'rrd_id':'№',
                    'gi_id': 'Номер поставки',
                    'subject_name': 'Предмет',
                    'nm_id': 'Код номенклатуры',
                    'brand_name': 'Бренд',
                    'sa_name': 'Артикул поставщика',
                    'ts_name': 'Размер',
                    'barcode': 'Баркод',
                    'doc_type_name': 'Тип документа',
                    'quantity': 'Кол-во',
                    'retail_price': 'Цена розничная',
                    'retail_amount': 'Вайлдберриз реализовал товар (Пр)',
                    'sale_percent': 'Согласованный продуктовый дисконт, %',
                    'commission_percent': 'Размер кВВ, %',
                    'office_name': 'Склад',
                    'supplier_oper_name': 'Обоснавние для оплаты',
                    'order_dt':	'Дата заказа покупателем',
                    'sale_dt': 'Дата продажи',
                    'rr_dt': 'Какая-то дата',
                    'shk_id': 'ШК',
                    'retail_price_withdisc_rub': 'Цена розничная с учетом согласованной скидки',
                    'delivery_amount': 'Количество доставок',
                    'return_amount': 'Количество возврата',
                    'delivery_rub': 'Услуги по доставке товара покупателю',
                    'gi_box_type_name': 'Тип коробов',
                    'product_discount_for_report': 'Итоговая согласованная скидка',
                    'supplier_promo': 'Supplier promo',
                    'rid': 'Rid',
                    'sup_rating_prc_up': 'sup_rating_prc_up',
                    'is_kgvp_v2': 'is_kgvp_v2',
                    'ppvz_for_pay': 'К пречислению продавцу за реализованный товар',
                    'ppvz_vw': 'Вознаграждение Вайлдберриз (ВВ), без НДС',
                    'ppvz_vw_nds': 'НДС с вознакграждения Вайлдберриз',
                    'sticker_id': 'Стикер МП',
                    'site_country': 'Страна',
                    'penalty': 'Общая сумма штрафов',
                    'additional_payment': 'Доплаты',
                    'rebill_logistic_cost': 'Возмещение издержек по перевозке',
                    'rebill_logistic_org': 'Организатор перевозки',
                    'srid': 'Srid',
                    'ppvz_spp_prc': 'Скидка постоянного покупателя',
                    'ppvz_kvw_prc_base': 'Размер кВВ без НДС, % Базовый',
                    'ppvz_kvw_prc': 'Итоговый кВВ без НДС, %',
                    'ppvz_sales_commission': 'Вознаграждение с продаж до вычета услуг поверенного, без НДС',
                    'ppvz_reward': 'Возмещение за выдачу и возврат товаров на ПВЗ',
                    'acquiring_fee': 'Возмещение издержек по эквайрингу',
                    'acquiring_bank': 'Наименование банка-эквайера',
                    'ppvz_office_id': 'Номер офиса',
                    'ppvz_supplier_id': 'ppvz_supplier_id',
                    'ppvz_supplier_name': 'Партнер',
                    'ppvz_inn': 'ИНН партнера',
                    'declaration_number': 'Номер таможенной декларации',
                    'ppvz_office_name': 'Наименование офиса доставки',
                    'bonus_type_name': 'bonus_type_name'
                }
            )
            heads = df.columns.tolist()
            values = df.values.tolist()
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = "attachment;filename=report.csv"
            writer = csv.writer(response)
            writer.writerow(heads)
            for row in values:
                writer.writerow(row)
            return response
    context['form'] = form
    return render(request, template, context)
