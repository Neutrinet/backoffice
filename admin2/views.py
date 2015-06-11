from django.shortcuts import render
from django.db.models import Sum

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
