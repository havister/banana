from django.db import models
from django.utils import timezone
from pointnut.commons import ChoiceInfo


class Launch(models.Model):
    name = models.CharField(max_length=30)
    gender_choice = models.CharField(max_length=1, choices=ChoiceInfo.GENDER_CHOICES)    
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

    @property
    def masked_name(self):
        return f'{self.name[:2]}*'

    @property
    def gender(self):
        return ChoiceInfo.GENDERS[self.gender_choice]

    @property
    def masked_phone(self):
        part_one = self.phone[:3]
        part_three = self.phone[-4:]
        return f'{part_one}-****-{part_three}'
