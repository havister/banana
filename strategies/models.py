from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from pointnut.commons import ChoiceInfo
from markets.models import Index, Stock, Etf, Future


class Strategy(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)
    summary = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='strategies')
    price = models.DecimalField(max_digits=8, decimal_places=0)
    long_positions = models.PositiveSmallIntegerField()
    short_positions = models.PositiveSmallIntegerField(default=0)
    date_created = models.DateField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "strategies"

    def __str__(self):
        return self.name


class Signal(models.Model):
    strategy = models.ForeignKey(Strategy, on_delete=models.CASCADE, related_name='signals')
    index_asset = models.ForeignKey(Index, on_delete=models.CASCADE, null=True, blank=True, related_name='signals_asset')
    stock_asset = models.ForeignKey(Stock, on_delete=models.CASCADE, null=True, blank=True, related_name='signals_asset')
    long_stock = models.ForeignKey(Stock, on_delete=models.CASCADE, null=True, blank=True, related_name='signals_long')
    long_etf = models.ForeignKey(Etf, on_delete=models.CASCADE, null=True, blank=True, related_name='signals_long')
    short_etf = models.ForeignKey(Etf, on_delete=models.CASCADE, null=True, blank=True, related_name='signals_short')
    short_future = models.ForeignKey(Future, on_delete=models.CASCADE, null=True, blank=True, related_name='signals_short')
    total_amount = models.DecimalField(max_digits=10, decimal_places=0)
    unit_amount = models.DecimalField(max_digits=8, decimal_places=0)
    date_created = models.DateField(default=timezone.now)
    date_updated = models.DateField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.strategy} | {self.asset}'

    @property
    def asset(self):
        asset = self.index_asset if self.index_asset else self.stock_asset
        return f'{asset}'

    @property
    def long_item(self):
        long_item = self.long_etf if self.long_etf else self.long_stock
        return f'{long_item}'

    @property
    def short_item(self):
        short_item = self.short_etf if self.short_etf else self.short_future
        return f'{short_item}'


class Watch(models.Model):
    signal = models.ForeignKey(Signal, on_delete=models.CASCADE, related_name='watches')
    price = models.DecimalField(max_digits=9, decimal_places=2)
    price_touched = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    condition_choice = models.CharField(max_length=1, choices=ChoiceInfo.CONDITION_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    date_started = models.DateField(default=timezone.now)
    date_touched = models.DateTimeField(null=True, blank=True)
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.signal} | {self.price} {self.condition}'

    @property
    def condition(self):
        return ChoiceInfo.CONDITIONS[self.condition_choice]


class Order(models.Model):
    watch = models.ForeignKey(Watch, on_delete=models.CASCADE, related_name='orders')
    level = models.PositiveSmallIntegerField()
    position_choice = models.CharField(max_length=1, choices=ChoiceInfo.POSITION_CHOICES)
    piece = models.PositiveSmallIntegerField()
    status_choice = models.CharField(max_length=1, choices=ChoiceInfo.STATUS_CHOICES)
    order_choice = models.CharField(max_length=1, choices=ChoiceInfo.ORDER_CHOICES)
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.watch} | {self.level}-{self.position}-{self.piece}'

    @property
    def position(self):
        return ChoiceInfo.POSITIONS[self.position_choice]
    
    @property
    def status(self):
        return ChoiceInfo.STATUSES[self.status_choice]

    @property
    def order(self):
        return ChoiceInfo.ORDERS[self.order_choice]
    