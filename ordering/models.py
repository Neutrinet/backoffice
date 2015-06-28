from datetime import datetime, date, timedelta

from django.db import models


COUNTRIES = (
    ('be', 'Belgium'),
    ('nl', 'Netherlands'),
    ('lu', 'Luxembourg'),
)


class GroupOrder(models.Model):
    launched_on = models.DateTimeField(auto_now_add=True)

    group_order_state = (
        ('open', 'Open'),
        ('close', 'Close'),
        ('done', 'Done'),
    )

    name = models.CharField(max_length=255)
    state = models.CharField(max_length=15, choices=group_order_state, default="open")
    description = models.TextField(null=True, blank=True)
    deadline = models.DateField(null=True, blank=True)
    number = models.PositiveSmallIntegerField()

    @classmethod
    def get_next_group_order_number(self):
        group_orders = GroupOrder.objects.order_by("-launched_on")

        if not group_orders.exists():
            return 1
        else:
            return group_orders.first().number + 1

    @classmethod
    def generate_next_group_order_name(self):
        group_orders = GroupOrder.objects.order_by("-launched_on")

        number = GroupOrder.get_next_group_order_number()

        if not group_orders.exists() or not group_orders.first().deadline:
            today = date.today()
            next_month = today.replace(day=1) + timedelta(days=31)
        else:
            next_month = group_orders.first().deadline.replace(day=1) + timedelta(days=31)

        return "Group Order #%s %s" % (number, next_month.strftime("%B %Y"))

    @classmethod
    def close_deadline_passed_grouper_order(klass):
        GroupOrder.objects.filter(deadline__isnull=False, deadline__gt=date.today(), state="open").update(state="close")

    def __unicode__(self):
        return u"%s [%s]" % (self.name, self.state)


class Order(models.Model):
    made_on = models.DateTimeField(auto_now_add=True)

    group_order = models.ForeignKey(GroupOrder, null=True, blank=True)

    nick = models.CharField(max_length=255, null=True, blank=True, verbose_name="Nickname (optional)", help_text="We may know you better by your nickname than your civil name :-)")
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    email = models.EmailField(help_text="We will never send you unwanted emails. You will only receive a copy of your order, and further information about it.")

    wants_vpn = models.BooleanField(default=False, verbose_name="I want to subscribe to the Neutrinet's VPN service and become a member of Neutrinet ASBL/VZW")
    wants_to_install_everything_himself = models.BooleanField(default=False, verbose_name="Do not configure my Cube for me, I want to do it by myself")

    # domain
    wants_neutrinet_to_renew_the_domain = models.BooleanField(default=False, verbose_name="I want my domain to be renewed automatically every year.", help_text="It is a common mistake to forget to renew a domain name every year. Check this box if you want Neutrinet to do it for you.")
    domain_name = models.CharField(max_length=255, blank=True, null=False, verbose_name="Domain name")

    # needed if the user wants the vpn
    street = models.CharField(max_length=255, null=True, blank=True)
    postal_code = models.CharField(max_length=255, null=True, blank=True)
    town = models.CharField(max_length=255, null=True, blank=True)
    birthplace = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=2, choices=COUNTRIES, null=True, blank=True, help_text="If you do not see your country of living on this list, please <a href='http://db.ffdn.org'>find another ISP closer to you</a>. If you want to choose Neutrinet anyway, please indicate your country of living in the comment section below.")
    birth_date = models.DateField(null=True, blank=True, help_text="Format: dd/mm/yyyy")

    # private
    has_payed = models.BooleanField(default=False)
    we_have_received_the_order = models.BooleanField(default=False)
    member_has_been_give_order = models.BooleanField(default=False)
    private_comment = models.TextField(null=True, blank=True)

    components = models.ManyToManyField('Component', through='ComponentOrder')

    estimated_price = models.DecimalField(max_digits=10, decimal_places=2)
    real_price = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2)
    # member is invited to add more if he wants to
    price_payed = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2)

    comment = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return u"order #%s for %s made %s days ago" % (self.id, "%s %s" % (self.first_name, self.last_name) if not self.nick else "%s %s (%s)" % (self.first_name, self.last_name, self.nick), (datetime.now() - self.made_on.replace(tzinfo=None)).days)

    def save(self, *args, **kwargs):
        if self.group_order is None:
            if not GroupOrder.objects.filter(state="open").exists():
                self.group_order = GroupOrder.objects.create(
                    name=GroupOrder.generate_next_group_order_name(),
                    state="open",
                    number=GroupOrder.get_next_group_order_number(),
                )
            else:
                self.group_order = GroupOrder.objects.filter(state="open").first()

        return super(Order, self).save(*args, **kwargs)


class Component(models.Model):
    reference = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)  # price costing right now (default is for ordering >= 10)
    url = models.URLField()
    estimated_shipment_time = models.PositiveSmallIntegerField(null=True, blank=True, help_text="in days")
    in_default_pack = models.BooleanField(default=False)

    @property
    def provider(self):
        return self.url.split("//")[1].split("/")[0].replace("www.", "").replace(".com", "")

    def display_with_url(self):
        return '<a href="%s">%s</a>' % (self.url, self)

    def __unicode__(self):
        return self.reference if not self.full_name else u"%s (%s)" % (self.full_name, self.reference)


class ComponentOrder(models.Model):
    order = models.ForeignKey(Order)
    component = models.ForeignKey(Component)
    number = models.PositiveIntegerField(default=1)
    paid_price = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2)  # effectivly paid price
    received = models.PositiveIntegerField(default=0)

    @property
    def price(self):
        return self.paid_price if self.paid_price else self.component.current_price

    @property
    def total_price(self):
        return self.number * self.price

    def __unicode__(self):
        return u"%s '%s' for %s" % (self.number, self.component, self.order)
