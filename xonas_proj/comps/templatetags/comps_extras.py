from django import template

register = template.Library()


def get_price(dic, key):
    return dic[key]['median_price']


def get_stocks_tag(dic, key):
    return dic[key]['stocks']


def get_sales_tag(dic, key):
    return dic[key]['avg_sales']


def get_sales_graph(dic, key):
    return dic[key]['sells_list']


def get_stocks_graph(dic, key):
    return dic[key]['stocks_list']


register.filter('get_price', get_price)
register.filter('get_stocks_tag', get_stocks_tag)
register.filter('get_sales_tag', get_sales_tag)
register.filter('get_sales_graph', get_sales_graph)
register.filter('get_stocks_graph', get_stocks_graph)
