from django.shortcuts import render
from django.db.models import Sum

from ordering.models import Order, Component


def current_order(request):
    return render(request, "admin2/current_order.haml", {
        "orders": Order.get_current(),
        "new_vpn_subscription": Order.get_current().filter(wants_vpn=True).count(),
        "components": Component.objects.filter(componentorder__order=Order.get_current()).distinct(),
        "total_estimated_price": Order.objects.aggregate(Sum('estimated_price'))['estimated_price__sum'],
    })
