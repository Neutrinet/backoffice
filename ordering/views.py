from django.shortcuts import render

from .models import Component
from .forms import OrderForm


def make_order(request):
    return render(request, "order.haml", {
        "form": OrderForm(),
        "default_components": Component.objects.filter(in_default_pack=True),
        "other_components": Component.objects.filter(in_default_pack=False),
    })
