from django.contrib import admin
from strategies import models

admin.site.register(models.Strategy)
admin.site.register(models.Signal)
admin.site.register(models.Watch)
admin.site.register(models.Order)
