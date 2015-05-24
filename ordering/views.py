from django.shortcuts import render


def make_order(request):
    return render(request, "order.haml")
