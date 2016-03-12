from django import template
from django.db.models import Sum


register = template.Library()


@register.simple_tag
def componentorder_sum(component_list, orders):
    return sum([count_in_current_group_order(x, orders) for x in component_list])


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
    real_price__sum = orders.filter(price_payed__isnull=False).aggregate(Sum('real_price'))["real_price__sum"]
    estimated_price__sum = orders.filter(price_payed__isnull=False).aggregate(Sum('estimated_price'))["estimated_price__sum"]
    price_payed__sum = orders.filter(price_payed__isnull=False).aggregate(Sum('price_payed'))["price_payed__sum"]

    if price_payed__sum is None and estimated_price__sum is None:
        return 0
    if real_price__sum is None:
        return price_payed__sum - estimated_price__sum
    else:
        return price_payed__sum - real_price__sum


@register.simple_tag
def count_in_current_group_order(component, orders):
    return component.componentorder_set.filter(order=orders).aggregate(Sum('number'))['number__sum']


@register.simple_tag
def prices_in_current_group_order(component, orders):
    prices = set([x.price for x in component.componentorder_set.filter(order=orders)])
    if len(prices) == 1:
        for i in prices:
            return i

    return prices
