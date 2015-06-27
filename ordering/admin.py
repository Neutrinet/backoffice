import reversion

from django.contrib import admin
from .models import GroupOrder, Order, Component, ComponentOrder


class OrderInline(admin.TabularInline):
    model = Order
    extra = 1


class GroupOrderAdmin(reversion.VersionAdmin):
    inlines = (OrderInline,)


class ComponentOrderInline(admin.TabularInline):
    model = ComponentOrder
    extra = 1


class OrderAdmin(reversion.VersionAdmin):
    readonly_fields = ('made_on',)
    inlines = (ComponentOrderInline,)
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
        ('Domain Name', {
            'fields': (('wants_neutrinet_to_renew_the_domain', 'domain_name'),)
        }),
        ('Status informations', {
            'fields': (('estimated_price', 'real_price'), ('has_payed', 'price_payed'), ('member_has_been_give_order', 'we_have_received_the_order'))
        }),
        ('Additional informations', {
            'fields': ('comment', 'private_comment'),
        }),
    )


class ComponentAdmin(reversion.VersionAdmin):
    list_display = ('__unicode__', 'current_price', 'in_default_pack')


admin.site.register(GroupOrder, GroupOrderAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Component, ComponentAdmin)
