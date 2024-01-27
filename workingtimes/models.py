from django.db import models
from shops.models import Shop


class WorkingTime(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    WEEKDAYS = [
        (1, "Monday"),
        (2, "Tuesday"),
        (3, "Wednesday"),
        (4, "Thursday"),
        (5, "Friday"),
        (6, "Saturday"),
        (7, "Sunday"),
    ]
    day = models.IntegerField(choices=WEEKDAYS, blank=False)
    opens = models.TimeField(default='09:00:00', blank=False, help_text='Example: 09:00:00')
    closes = models.TimeField(default='23:00:00', blank=False, help_text='Example: 23:59:00')

    class Meta:
        ordering = ('day', 'opens')

    def __str__(self):
        return f'{self.day}\t {self.opens}\t {self.closes}'
