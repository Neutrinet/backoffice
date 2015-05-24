import reversion

from django.contrib import admin
from .models import Order, Component


class OrderAdmin(reversion.VersionAdmin):
    pass


class ComponentAdmin(reversion.VersionAdmin):
    pass


admin.site.register(Order, OrderAdmin)
admin.site.register(Component, ComponentAdmin)
