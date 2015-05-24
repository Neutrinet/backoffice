from datetime import datetime

from django.db import models


COUNTRIES = (
    ('be', 'Belgium'),
    ('nl', 'Netherlands'),
    ('lu', 'Luxembourg'),
)

class Order(models.Model):
    made_on = models.DateTimeField(auto_now_add=True)

    nick = models.CharField(max_length=255, null=True, blank=True, verbose_name="Nick (optional)", help_text="remember that we know some of you better by nick than by civil name, help use make the association")
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    email = models.EmailField(help_text="To be able to contact you to inform you that your order is here. We'll never send you unsolicited emails.")

    wants_vpn = models.BooleanField(default=False, verbose_name="I want to apply to a VPN subscription  at Neutrinet for my cube (and therefor became a member of Neutrinet)")
    wants_to_install_everything_himself = models.BooleanField(default=False, verbose_name="Don't configure anything for me, I want to do everything by myself")

    # domain
    wants_neutrinet_to_renew_the_domain = models.BooleanField(default=False, verbose_name="I want Neutrinet to take care of renewing my domain name for me.", help_text="A domain name fee must be paid every year, it's a common mistake to forget to renew it and lost your domain name, we offer to take care of this for you.")
    domain_name = models.URLField(blank=True, null=False, verbose_name="Domain name (optional)")

    # needed if the user wants the vpn
    street = models.CharField(max_length=255, null=True, blank=True)
    postal_code = models.CharField(max_length=255, null=True, blank=True)
    town = models.CharField(max_length=255, null=True, blank=True)
    birthplace = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=2, choices=COUNTRIES, null=True, blank=True, help_text="If you don't see your country, please look for another ISP on <a href='http://db.ffdn.org'>db.ffdn.org</a>. If you still want to choose Neutrinet, please indicate your country in the comment section bellow.")
    birth_date = models.DateField(null=True, blank=True)

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
        return "order #%s for %s made %s days ago" % (self.id, "%s %s" % (self.first_name, self.last_name) if not self.nick else "%s %s (%s)" % (self.first_name, self.last_name, self.nick), (datetime.now() - self.made_on.replace(tzinfo=None)).days)


class Component(models.Model):
    reference = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)  # price costing right now (default is for ordering >= 10)
    url = models.URLField()
    estimated_shipment_time = models.PositiveSmallIntegerField(null=True, blank=True, help_text="in days")
    in_default_pack = models.BooleanField(default=False)

    def __unicode__(self):
        return self.reference if not self.full_name else u"%s (%s)" % (self.full_name, self.reference)


class ComponentOrder(models.Model):
    order = models.ForeignKey(Order)
    component = models.ForeignKey(Component)
    number = models.PositiveIntegerField(default=1)
    paid_price = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2)  # effectivly paid price
    received = models.PositiveIntegerField(default=0)

    def __unicode__(self):
        return "%s '%s' for %s" % (self.number, self.component, self.order)
