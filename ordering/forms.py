from django import forms

from .models import Order, Component


class OrderForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)

        for component in Component.objects.all():
            self.fields["component_%s_number" % component.id] = forms.IntegerField(min_value=0)

        self.fields["birth_date"].input_formats = ['%Y-%m-%d', '%d/%m/%Y', '%d/%m/%y']

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

            'estimated_price', # I should add it myself I think

            'comment'
        )
