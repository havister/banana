from django.contrib import admin
from markets import models

admin.site.register(models.Expiration)
admin.site.register(models.Index)
admin.site.register(models.Stock)
admin.site.register(models.Etf)
admin.site.register(models.Future)
