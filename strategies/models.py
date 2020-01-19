from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from pointnut.commons import ChoiceInfo
from markets.models import Index, Stock, Etf


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
    long_etf = models.ForeignKey(Etf, on_delete=models.CASCADE, null=True, blank=True, related_name='signals_long')
    short_etf = models.ForeignKey(Etf, on_delete=models.CASCADE, null=True, blank=True, related_name='signals_short')
    total_amount = models.DecimalField(max_digits=10, decimal_places=0)
    unit_amount = models.DecimalField(max_digits=8, decimal_places=0)
    date_created = models.DateField(default=timezone.now)
    date_updated = models.DateField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.strategy} | {self.asset} | {"{:,}".format(self.total_amount)}'

    @property
    def is_index(self):
        is_index = True if self.index_asset else False
        return is_index

    @property
    def asset(self):
        asset = self.index_asset if self.index_asset else self.stock_asset
        return f'{asset}'

    @property
    def asset_code(self):
        asset = self.index_asset if self.index_asset else self.stock_asset
        return f'{asset.code}'

    @property
    def long_item(self):
        long_item = f'{self.long_etf}' if self.long_etf else ""
        return long_item

    @property
    def long_code(self):
        long_code = self.long_etf.code if self.long_etf else ""
        return long_code

    @property
    def short_item(self):
        short_item = f'{self.short_etf}' if self.short_etf else ""
        return short_item

    @property
    def short_code(self):
        short_code = self.short_etf.code if self.short_etf else ""
        return short_code

    @property
    def as_json_dict(self):
        data = {
            'Pk': self.pk,
            'Strategy': self.strategy.name,
            'Asset': self.asset,
            'AssetCode': self.asset_code,
            'LongItem': self.long_item,
            'LongCode': self.long_code,
            'ShortItem': self.short_item,
            'ShortCode': self.short_code,
            'UnitAmount': int(self.unit_amount)
        }
        return data


class Watch(models.Model):
    signal = models.ForeignKey(Signal, on_delete=models.CASCADE, related_name='watches')
    price = models.DecimalField(max_digits=9, decimal_places=2)
    price_touched = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    condition_choice = models.CharField(max_length=1, choices=ChoiceInfo.CONDITION_CHOICES)
    date_started = models.DateField(default=timezone.now)
    date_touched = models.DateTimeField(null=True, blank=True)
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "watches"

    def __str__(self):
        return f'{self.signal} | {self.price} | {self.condition}'

    @property
    def condition(self):
        return ChoiceInfo.CONDITIONS[self.condition_choice]

    @property
    def as_json_dict(self):
        data = {
            'Pk': self.pk,
            'Price': float(self.price),
            'Condition': self.condition_choice,
        }
        return data


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
        return f'{self.watch} | {self.level}-{self.position}-{self.piece} | {self.status} | {self.order}'

    @property
    def position(self):
        return ChoiceInfo.POSITIONS[self.position_choice]
    
    @property
    def status(self):
        return ChoiceInfo.STATUSES[self.status_choice]

    @property
    def order(self):
        return ChoiceInfo.ORDERS[self.order_choice]

    @property
    def as_json_dict(self):
        data = {
            'Level': self.level,
            'Position': self.position_choice,
            'Piece': self.piece,
            'Status': self.status_choice,
            'Order': self.order_choice,
            'Quantity': 0
        }
        return data
