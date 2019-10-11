from django.db import models
from django.utils import timezone


class Launch(models.Model):
    # Gender choices
    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female')
    ]
    name = models.CharField(max_length=30)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)    
    age = models.PositiveSmallIntegerField()
    phone = models.CharField(max_length=11)
    is_married = models.BooleanField(default=False)
    job = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    has_fund = models.BooleanField(default=False)
    has_stock = models.BooleanField(default=False)
    has_derivative = models.BooleanField(default=False)
    recommender = models.CharField(max_length=30)
    date_submitted = models.DateTimeField(default=timezone.now)
    date_been_tester = models.DateField(null=True, blank=True)
    date_been_observer = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "launches"

    def __str__(self):
        return self.name
