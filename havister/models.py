from django.db import models
from django.contrib.auth.models import User


class Log(models.Model):
    player = models.ForeignKey(User, on_delete=models.CASCADE, related_name='logs')
    message = models.CharField(max_length=200)
    code = models.CharField(max_length=20, null=True, blank=True)
    datetime = models.DateTimeField()

    def __str__(self):
        return f'{self.player} | {self.datetime}'

    @property
    def time_message(self):
        time = self.datetime.strftime('%H:%M:%S')
        return f'{time} | {self.message}'
