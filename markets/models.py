from django.db import models
from django.utils import timezone


class Expiration(models.Model):
    code = models.CharField(max_length=4, primary_key=True)
    date_expired = models.DateField(default=timezone.now)

    def __str__(self):
        return f'{self.code[:2]}년 {self.code[2:]}월'


class Index(models.Model):
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=20, unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "indexes"
    
    def __str__(self):
        return self.name


class Stock(models.Model):
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=20, unique=True)
    has_future = models.BooleanField(default=False)
    has_option = models.BooleanField(default=False)
    is_kospi = models.BooleanField(default=False)
    is_kospi_200 = models.BooleanField(default=False)
    is_kospi_100 = models.BooleanField(default=False)
    is_kospi_50 = models.BooleanField(default=False)
    is_kosdaq = models.BooleanField(default=False)
    is_kosdaq_150 = models.BooleanField(default=False)
    is_primary = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Etf(models.Model):
    index = models.ForeignKey(Index, on_delete=models.CASCADE, related_name='etfs')
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=20, unique=True)
    is_inverse = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Future(models.Model):
    index_asset = models.ForeignKey(Index, on_delete=models.CASCADE, null=True, blank=True, related_name='futures')
    stock_asset = models.ForeignKey(Stock, on_delete=models.CASCADE, null=True, blank=True, related_name='futures')
    code = models.CharField(max_length=20, unique=True)
    expiration = models.ForeignKey(Expiration, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        asset = self.index_asset if self.index_asset else self.stock_asset
        return f'{asset.name} F {self.expiration.code}'
