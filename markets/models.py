from django.db import models
from django.utils import timezone


class Market(models.Model): 
    date = models.DateField()
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    is_holiday = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.date}'


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
