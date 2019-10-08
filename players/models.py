from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from markets.models import Asset
from signals.models import Signal


class Account(models.Model):
    STOCK = '01'
    DERIVATIVE = '03'
    CATEGORY_CHOICES = [
        (STOCK, 'Stock'),
        (DERIVATIVE, 'Derivative')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    number = models.CharField(max_length=11)
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES)
    password = models.CharField(max_length=128)
    fund = models.DecimalField(max_digits=10, decimal_places=0)
    is_active = models.BooleanField(default=True)
    date_bound = models.DateField(default=timezone.now)

    def __str__(self):
        return f'{self.number}-{self.category}'


class Trade(models.Model):
    # Position choices
    LONG = 'L'
    SHORT = 'S'
    POSITION_CHOICES = [
        (LONG, 'Long'),
        (SHORT, 'Short'),
    ]
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    signal = models.ForeignKey(Signal, on_delete=models.CASCADE)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    position = models.CharField(max_length=1, choices=POSITION_CHOICES)
    date_opened = models.DateTimeField(default=timezone.now)
    price_opened = models.DecimalField(max_digits=9, decimal_places=2)
    date_closed = models.DateTimeField(null=True, blank=True)
    price_closed = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    difference = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    change = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)

    def __str__(self):
        name = f'{self.asset}'
        return name
