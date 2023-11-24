from django import template

register = template.Library()


def get_graph(str):
    res = str.split(',')
    res = [int(x) for x in res]
    return res


register.filter('get_graph', get_graph)