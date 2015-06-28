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
    if orders.filter(has_payed=True).count() == 0:
        return 0

    return orders.filter(price_payed__isnull=False).aggregate(Sum('price_payed'))["price_payed__sum"]


@register.simple_tag
def total_addition_from_free_price(orders):
    if orders.filter(has_payed=True).count() == 0:
        return 0

    orders = orders.filter(has_payed=True)
    return orders.filter(price_payed__isnull=False).aggregate(Sum('price_payed'))["price_payed__sum"] - orders.filter(price_payed__isnull=False).aggregate(Sum('real_price'))["real_price__sum"]


@register.simple_tag
def count_in_current_group_order(component, group_order):
    return component.componentorder_set.filter(order=group_order).aggregate(Sum('number'))['number__sum']
