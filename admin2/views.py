from django.shortcuts import render
from django.db.models import Sum

from ordering.models import Order


def current_order(request):
    return render(request, "admin2/current_order.haml", {
        "orders": Order.get_current(),
        "total_estimated_price": Order.objects.aggregate(Sum('estimated_price'))['estimated_price__sum'],
    })
