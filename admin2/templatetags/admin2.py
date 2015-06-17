from django import template
from django.db.models import Sum


register = template.Library()


@register.simple_tag
def componentorder_sum(component_list):
    return sum([x.count_in_current_group_order() for x in component_list])


@register.simple_tag
def mail_space(string):
    return " " * (80 - len(unicode(string)))


@register.simple_tag
def total_payed(orders):
    return orders.filter(price_payed__isnull=False).aggregate(Sum('price_payed'))["price_payed__sum"]
