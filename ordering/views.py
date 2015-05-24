from django.shortcuts import render

from .forms import OrderForm


def make_order(request):
    return render(request, "order.haml", {
        "form": OrderForm()
    })
