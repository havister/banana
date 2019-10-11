from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from markets.models import Asset
from signals.models import Signal


class Account(models.Model):
    player = models.OneToOneField(User, on_delete=models.CASCADE, related_name='account')
    long_fund = models.DecimalField(max_digits=10, decimal_places=0)
    short_fund = models.DecimalField(max_digits=10, decimal_places=0)
    has_havister = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_bound = models.DateField(default=timezone.now)

    def __str__(self):
        return f'{self.player}'

"""
class Watch(models.Model):
    # Condition choices
    CONDITION_CHOICES = [
        ('U', 'Up'),
        ('D', 'Down'),
    ]
    player = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watches')
    signal = models.ForeignKey(Signal, on_delete=models.CASCADE, related_name='watches')
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='watches')
    target_price = models.DecimalField(max_digits=9, decimal_places=2)
    condition = models.CharField(max_length=1, choices=CONDITION_CHOICES)
    date_started = models.DateField(default=timezone.now)
    start_time = models.TimeField()
    end_time = models.TimeField()
    date_ended = models.DateField(null=True, blank=True)
    price_touched = models.DecimalField(max_digits=9, decimal_places=2)
    date_touched = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        name = f'{self.asset}'
        return name


class Order(models.Model):
    # Item choices
    ITEM_CHOICES = [
        ('S', 'Stock'),
        ('E', 'Etf'),
        ('F', 'Future'),
    ]
    # Trade choices
    TRADE_CHOICES = [
        ('B', 'Buy'),
        ('S', 'Sell'),
    ]
    watch = models.ForeignKey(Watch, on_delete=models.CASCADE, related_name='orders')
    item = models.CharField(max_length=1, choices=ITEM_CHOICES)
    code = models.CharField(max_length=20)
    trade = models.CharField(max_length=1, choices=TRADE_CHOICES)
    amount = models.DecimalField(max_digits=7, decimal_places=0)
    quantity = models.PositiveIntegerField(default=0)
    date_ordered = models.DateTimeField(default=timezone.now)
    date_traded = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        name = f'{self.watch.asset}'
        return name
    
"""
class Trade(models.Model):
    # Position choices
    POSITION_CHOICES = [
        ('L', 'Long'),
        ('S', 'Short'),
    ]
    player = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trades')
    signal = models.ForeignKey(Signal, on_delete=models.CASCADE, related_name='trades')
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='trades')
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
