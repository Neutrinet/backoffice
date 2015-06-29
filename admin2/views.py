from django.shortcuts import render, get_object_or_404
from django.db.models import Sum

from ordering.models import Component, GroupOrder


def group_order_detail(request, pk):
    group_order = get_object_or_404(GroupOrder, pk=pk)
    orders = group_order.order_set.all()
    components = Component.objects.filter(componentorder__order=orders).distinct()

    providers = set()
    for component in components:
        providers.add(component.provider)

    provider_order_list = [{
        "provider": provider,
        "orders": orders.filter(componentorder__component__url__icontains=provider).distinct(),
    } for provider in providers]

    return render(request, "admin2/current_order.haml", {
        "group_order": group_order,
        "orders": orders,
        "new_vpn_subscription": orders.filter(wants_vpn=True).count(),
        "components": components,
        "total_real_price": orders.aggregate(Sum('real_price'))['real_price__sum'],
        "total_estimated_price": orders.aggregate(Sum('estimated_price'))['estimated_price__sum'],
        "provider_order_list": provider_order_list,
    })
