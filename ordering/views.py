from django.shortcuts import render
from django.db import transaction
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from .models import Component, ComponentOrder
from .forms import OrderForm


def make_order(request):
    if request.method == "GET":
        return render(request, "order.haml", {
            "form": OrderForm(),
            "default_components": Component.objects.filter(in_default_pack=True),
            "other_components": Component.objects.filter(in_default_pack=False),
        })

    assert request.method == "POST"

    form = OrderForm(request.POST)

    print request.POST

    if not form.is_valid():
        return render(request, "order.haml", {
            "form": form,
            "default_components": Component.objects.filter(in_default_pack=True),
            "other_components": Component.objects.filter(in_default_pack=False),
        })

    with transaction.atomic():
        order = form.save()

        for component in Component.objects.all():
            if form.cleaned_data["component_%d_number" % component.id] > 0:
                ComponentOrder.objects.create(
                    order=order,
                    component=component,
                    number=form.cleaned_data["component_%d_number" % component.id]
                )

    # TODO send email

    return HttpResponseRedirect(reverse("success"))
