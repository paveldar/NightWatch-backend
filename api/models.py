from django.db import models
from django.contrib.auth.models import User


class Group(models.Model):
    participants = models.JSONField(default=list)
    date_from = models.DateField()
    date_to = models.DateField()
    time_from = models.TimeField()
    time_to = models.TimeField()
    night_count = models.PositiveSmallIntegerField(blank=True, default=0)
    duration = models.IntegerField(blank=True, default=0)
    shifts = models.JSONField(default=list, blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exp_group')

    def __str__(self):
        return f'{self.date_from} - {self.date_to}'
