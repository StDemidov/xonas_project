from django import template

register = template.Library()


def get_from_dict(dict, key):
    return dict[key]['median_price']


register.filter('get_from_dict', get_from_dict)
