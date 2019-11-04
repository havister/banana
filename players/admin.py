from django.contrib import admin
from players import models

admin.site.register(models.Account)
admin.site.register(models.Shopping)
admin.site.register(models.Play)
admin.site.register(models.Trade)
