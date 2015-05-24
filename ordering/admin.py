import reversion

from django.contrib import admin
from .models import Order, Component


class OrderAdmin(reversion.VersionAdmin):
    readonly_fields = ('made_on',)
    fieldsets = (
        (None, {
            'fields': ('made_on',)
        }),
        ('Member infos', {
            'fields': (('nick', 'email'), ('first_name', 'last_name'))
        }),
        ('Member preferences', {
            'fields': (('wants_vpn', 'wants_to_install_everything_himself'),)
        }),
        ('VPN informations', {
            'fields': (('street', 'postal_code'), ('town', 'country'), ('birthplace', 'birth_date'))
        }),
        ('Status informations', {
            'fields': (('estimated_price', 'real_price'), ('has_payed', 'price_payed'), ('member_has_been_give_order', 'we_have_received_the_order'))
        }),
        ('Additional informations', {
            'fields': ('comment', 'private_comment'),
        }),
    )


class ComponentAdmin(reversion.VersionAdmin):
    pass


admin.site.register(Order, OrderAdmin)
admin.site.register(Component, ComponentAdmin)
