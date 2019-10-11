from django.db import models
from django.utils import timezone
from markets.models import Asset


class Signal(models.Model):
    name = models.CharField(max_length=20)
    creator = models.CharField(max_length=20)
    assets = models.ManyToManyField(Asset, related_name='signals')
    is_active = models.BooleanField(default=True)
    date_created = models.DateField(default=timezone.now)

    def __str__(self):
        return self.name
