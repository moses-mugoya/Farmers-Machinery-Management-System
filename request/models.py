from django.db import models
from machine.models import Machine
from django.conf import settings
from django.core.validators import RegexValidator


class AboutRequest(models.Model):
    ADDRESS_OF_DELIVERY = (
        ('meru', 'Meru Town'),
        ('kianjai', 'Kianjai',),
        ('nkubu', 'Nkubu',),
        ('maua', 'Maua'),
        ('Nchiu', 'Nchiru'))
    created = models.DateTimeField(auto_now_add=True, null=True)
    modified = models.DateTimeField(auto_now=True, null=True)
    address_of_delivery = models.CharField(max_length=50, choices=ADDRESS_OF_DELIVERY, default='Meru Town')
    approved = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='order', on_delete=models.CASCADE, null=True)
    phone_number = models.CharField(max_length=13, blank=True)
    active = models.BooleanField(default=True)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        total = sum(item.get_cost() for item in self.details.all())
        return total


class Request(models.Model):
    order = models.ForeignKey(AboutRequest, related_name='details', on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='orders', on_delete=models.CASCADE, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    modified = models.DateTimeField(auto_now=True, null=True)
    product = models.ForeignKey(Machine, related_name='order_item', on_delete=models.CASCADE, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ('-quantity',)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity


