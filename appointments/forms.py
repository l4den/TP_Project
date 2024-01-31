from datetime import datetime, date, timedelta, time
from django.utils import timezone

from django import forms
from .models import Appointment
from services.models import Service


def validate_future_date(value):
    if value < timezone.now().date():
        raise forms.ValidationError('Please select a date in the future.')


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['services', 'date', 'start_time']

    services = forms.ModelMultipleChoiceField(
        queryset=Service.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    date = forms.DateField(
        widget=forms.DateInput(
            attrs={'type': 'date',
                   'min': str(timezone.now().date()),
                   'max': str((timezone.now() + timedelta(days=30)).date())}),
        help_text='Select a date',
        validators=[validate_future_date],

    )
    start_time = forms.TimeField(widget=forms.TimeInput(format='%H:%M'),
                                 initial=datetime.now().time(),
                                 help_text='Format: HH:MM (e.g., 09:15)'
                                 )

    # shop da e automaticaly filled in
    # prvicno selektiraniot datum da e denesniot datum
    # moze da se izberat samo Services koi pripagjaat na toj shop
    def __init__(self, *args, **kwargs):
        self.shop = kwargs.pop('shop', None)
        self.user = kwargs.pop('user', None)
        super(AppointmentForm, self).__init__(*args, **kwargs)
        self.fields['date'].initial = datetime.today().date()
        self.fields['services'].queryset = self.shop.service_set.all() if self.shop else Appointment.objects.none()

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        apt_date = cleaned_data.get('date')
        services = cleaned_data.get('services')
        shop = self.shop

        if shop and services and apt_date and start_time:
            # Dali shop raboti na denot vo nedelata dobien od datumot?
            day_of_week = apt_date.weekday() + 1
            if day_of_week not in shop.working_week_days():
                self.add_error('date', "The shop doesn't work on the selected date.")

            # Ako e Appointment za denes
            if apt_date == timezone.now().date():
                # Dali start_time e vo idnina?
                now = datetime.now()
                now_time = now.time()
                if start_time < now_time:
                    self.add_error('start_time', "You cannot book an appointment in the past.")

            # Dali start_time e vo rabotnoto vreme na toj den?
            opens, closes = shop.open_close_time_by_weekday(day_of_week)
            if not (opens < start_time < closes) and day_of_week in shop.working_week_days():
                self.add_error('start_time', "The shop is closed at that time.")

            # Dali end_time > opens za toj den?
            duration = timedelta()
            for service in self.cleaned_data['services']:
                duration += timedelta(hours=service.time_to_complete.hour,
                                      minutes=service.time_to_complete.minute)

            endtime = timedelta(hours=start_time.hour, minutes=start_time.minute) + duration
            end_datetime = datetime.combine(date.today(), time()) + endtime
            end_time = end_datetime.time()
            if not opens < end_time < closes and day_of_week in shop.working_week_days():
                self.add_error('start_time', "The end of the appointment is past the shop's closing time.")

            # Dali korisnikot ima zakazano drug termin koj sto se poklopuva so ovoj?
            if not self.user.user_is_free(apt_date, start_time, end_time):
                self.add_error('date', "You have another appointment booked at this time.")

            # Dali ima drugi Appointments na taa data vo toa vreme?
            if not shop.timeslot_is_free(apt_date, start_time, end_time):
                self.add_error('start_time', "There is another appointment booked at this time.")

            return cleaned_data

    def save(self, commit=True):
        appointment = super(AppointmentForm, self).save(commit=False)

        duration = timedelta()
        price_total = 0
        for service in self.cleaned_data['services']:
            duration += timedelta(hours=service.time_to_complete.hour,
                                  minutes=service.time_to_complete.minute)
            price_total += service.price

        start_time = self.cleaned_data['start_time']
        appointment.duration = duration
        appointment.total_price = price_total
        appointment.end_time = timedelta(hours=start_time.hour, minutes=start_time.minute) + duration

        if commit:
            appointment.save()

        return appointment
