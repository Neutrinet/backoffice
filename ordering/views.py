from django.core.mail import send_mail
from django.utils.translation import ugettext as _
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render, get_object_or_404
from django.db import transaction
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from .models import Component, ComponentOrder, Order, GroupOrder
from .forms import OrderForm


def home(request):
    GroupOrder.close_deadline_passed_grouper_order()
    return render(request, "home.haml", {
        "group_orders": GroupOrder.objects.order_by("-launched_on")[:2],
    })


def make_order(request):
    GroupOrder.close_deadline_passed_grouper_order()

    if request.method == "GET":
        return render(request, "order.haml", {
            "form": OrderForm(),
            "default_components": Component.objects.filter(in_default_pack=True, available=True),
            "other_components": Component.objects.filter(in_default_pack=False, available=True),
        })

    assert request.method == "POST"

    form = OrderForm(request.POST)

    print request.POST

    if not form.is_valid():
        print form.errors
        return render(request, "order.haml", {
            "form": form,
            "default_components": Component.objects.filter(in_default_pack=True, available=True),
            "other_components": Component.objects.filter(in_default_pack=False, available=True),
        })

    with transaction.atomic():
        order = form.save()

        for component in Component.objects.filter(available=True):
            if form.cleaned_data["component_%d_number" % component.id] > 0:
                ComponentOrder.objects.create(
                    order=order,
                    component=component,
                    number=form.cleaned_data["component_%d_number" % component.id]
                )

    send_mail(
        _(u'[Neutrinet] Order #%s for one or more Internet Cube') % order.id,
        get_template('email.txt').render(Context({"order": order})),
        'cube@neutrinet.be',
        [order.email],
        fail_silently=False,
    )

    send_mail(
        u'[cube order] Order #%s by %s %s (%s)' % (order.id, order.first_name, order.last_name, order.nick if order.nick else "no nick"),
        get_template('admin_email.txt').render(Context({"order": order})),
        'backoffice@neutrinet.be',
        ['hub-cube@neutrinet.be'],
        fail_silently=False,
    )

    return HttpResponseRedirect(reverse("success"))


def email_debug(request, pk):
    return render(request, "email.txt", {
        "order": get_object_or_404(Order, pk=pk),
    })


def admin_email_debug(request, pk):
    return render(request, "admin_email.txt", {
        "order": get_object_or_404(Order, pk=pk),
    })
