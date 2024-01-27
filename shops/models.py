from django.db import models
from accounts.models import Account


class Shop(models.Model):
    name = models.CharField(max_length=200, blank=False)
    description = models.TextField(max_length=250, blank=True, default='')
    location = models.CharField(max_length=150, blank=False, default='')
    location_link = models.CharField(max_length=150, blank=False, default='',
                                     help_text='Link od Google Maps od vasata adresa')
    logo = models.ImageField(upload_to='shop_logos', default='default.jpg', blank=True)
    owner = models.ForeignKey(Account, on_delete=models.CASCADE)

    def time_in_range(self, time, begin, end):
        if begin < time < end:
            return True
        return False

    def working_week_days(self):
        working_times = self.workingtime_set.all()
        working_days = [wt.day for wt in working_times if wt.opens != wt.closes]
        return working_days

    def open_close_time_by_weekday(self, weekday):
        working_day = self.workingtime_set.get(day=weekday)
        return working_day.opens, working_day.closes

    def timeslot_is_free(self, date, start, end):
        appointments = self.appointment_set.filter(date=date)

        for appt in appointments:
            if (self.time_in_range(start, appt.start_time, appt.end_time) or
                    self.time_in_range(end, appt.start_time, appt.end_time)):
                return False

            if start == appt.start_time or end == appt.end_time:
                return False
            # ako terminot preklopuva drug termin
            if start < appt.start_time and appt.end_time < end:
                return False

        return True

    def __str__(self):
        return self.name
