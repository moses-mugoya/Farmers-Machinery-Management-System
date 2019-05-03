from django import forms
from .models import AboutRequest
from django.utils.translation import gettext_lazy as _

ADDRESS_OF_DELIVERY = (
        ('meru', 'Meru Town'),
        ('kianjai', 'Kianjai',),
        ('nkubu', 'Nkubu',),
        ('maua', 'Maua'),
        ('Nchiu', 'Nchiru'))


class OrderCreateForm(forms.ModelForm):
    address_of_delivery = forms.TypedChoiceField(
        widget=forms.Select(attrs={'class': 'form-control'}),
        label=_('Please choose your address of delivery'),
        label_suffix="",
        choices=ADDRESS_OF_DELIVERY)
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+254#########'}),
                                   label=_('Please enter the M-PESA number to receive notification about your request'),
                                   label_suffix="",
                                   max_length=13,
                                   min_length=13)

    class Meta:
        model = AboutRequest
        fields = ('address_of_delivery', 'phone_number')
