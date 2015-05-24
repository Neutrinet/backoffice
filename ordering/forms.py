from django import forms

from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = (
            'nick',
            'first_name',
            'last_name',
            'email',

            'wants_vpn',
            'wants_to_install_everything_himself',

            'wants_neutrinet_to_renew_the_domain',
            'domain_name',

            # needed if the user wants the vpn,
            'street',
            'postal_code',
            'town',
            'birthplace',
            'country',
            'birth_date',

            'components',

            'estimated_price', # I should add it myself I think

            'comment'
        )
