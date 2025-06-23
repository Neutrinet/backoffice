from smtplib import SMTP

from dns.name import NoParent
from dns.resolver import resolve

from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from .models import Component, Order


class OrderForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)

        for component in Component.objects.filter(available=True):
            self.fields["component_%s_number" % component.id] = forms.IntegerField(
                min_value=0
            )

        self.fields["birth_date"].input_formats = ["%Y-%m-%d", "%d/%m/%Y", "%d/%m/%y"]

    class Meta:
        model = Order
        fields = (
            "nick",
            "first_name",
            "last_name",
            "email",
            "wants_vpn",
            "wants_to_install_everything_himself",
            "wants_neutrinet_to_renew_the_domain",
            "domain_name",
            # needed if the user wants the vpn,
            "street",
            "postal_code",
            "town",
            "birthplace",
            "country",
            "birth_date",
            "estimated_price",  # I should add it myself I think
            "comment",
        )

    def clean_email(self):
        email = self.cleaned_data["email"]

        validate_email(email)

        _, domain = email.split("@")
        records = resolve(domain, "MX")
        mx_record = records[0].exchange
        try:
            mx_record.parent()
        except NoParent:
            raise ValidationError(
                f"Domain {domain} for email {email} has no MX record."
            )

        # SMTP lib setup (use debug level for full output)
        server = SMTP()
        server.set_debuglevel(0)

        # SMTP Conversation
        server.connect(mx_record.to_text())
        server.helo(settings.EMAIL_HOST)
        server.mail(settings.EMAIL_FROM)
        code, message = server.rcpt(email)
        server.quit()

        if code != 250:
            raise ValidationError(
                f"Domain {domain} for email {email} is not a valid mail server."
            )
