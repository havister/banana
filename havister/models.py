from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    player = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    level = models.CharField(max_length=20, null=True, blank=True)
    text = models.CharField(max_length=200)
    datetime = models.DateTimeField()

    def __str__(self):
        return f'{self.player} | {self.datetime}'

    @property
    def time_str(self):
        time = self.datetime.strftime('%H:%M:%S')
        return f'{time} | {self.text}'
