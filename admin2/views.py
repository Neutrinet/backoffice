from decimal import Decimal

from django.shortcuts import render
from django.db.models import Sum
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from ordering.models import Order, Component


def current_order(request):
    components = Component.objects.filter(componentorder__order=Order.get_current()).distinct()

    providers = set()
    for component in components:
        providers.add(component.provider)

    provider_order_list = [{
        "provider": provider,
        "orders": Order.get_current().filter(componentorder__component__url__icontains=provider).distinct(),
    } for provider in providers]

    return render(request, "admin2/current_order.haml", {
        "orders": Order.get_current(),
        "new_vpn_subscription": Order.get_current().filter(wants_vpn=True).count(),
        "components": components,
        "total_estimated_price": Order.objects.aggregate(Sum('estimated_price'))['estimated_price__sum'],
        "provider_order_list": provider_order_list,
    })


def calculate_final_price_for_current_order(request):
    # this function is mostly an hack for now

    for order in Order.get_current():
        # XXX hack
        # splited shipment cost for this order
        total = Decimal(1.25)

        for component_order in order.componentorder_set.all():
            total += component_order.price * component_order.number

        order.real_price = total
        order.save()

    return HttpResponseRedirect(reverse('admin2_current_order'))
