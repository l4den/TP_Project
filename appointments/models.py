from django.db import models
from django.utils import timezone
from shops.models import Shop
from accounts.models import Account
from services.models import Service
from datetime import date, timedelta, datetime
from django.core.validators import MinValueValidator, MaxValueValidator


class Appointment(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    date = models.DateField(default=date.today(),
                            help_text='eg. 23-11-2023',
                            validators=[MinValueValidator(date.today()),
                                        MaxValueValidator(date.today() + timedelta(days=30))])

    start_time = models.TimeField(blank=False, default=timezone.now)
    duration = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    services = models.ManyToManyField(Service)
    total_price = models.PositiveIntegerField(default=1, blank=True, null=True)

    def calculate_duration(self):
        total_duration = timedelta()
        for serv in self.services.all():
            total_duration += timedelta(hours=serv.time_to_complete.hour,
                                        minutes=serv.time_to_complete.minute)
        return total_duration

    def calculate_end_time(self):
        end_time = timedelta(hours=self.start_time.hour, minutes=self.start_time.minute) + self.calculate_duration()
        return end_time

    def calculate_total_price(self):
        total_price = sum(serv.price for serv in self.services.all())
        return total_price

    def __str__(self):
        return self.shop.name + ' ' + self.user.email + ' ' +  str(self.date)