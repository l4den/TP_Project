from datetime import datetime, date, timedelta, time

from django import forms
from .models import Appointment
from services.models import Service


def validate_future_date(value):
    if value < date.today():
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
            attrs={'type': 'date', 'min': str(date.today()), 'max': str(date.today() + timedelta(days=30))}),
        # Use the DateInput widget
        help_text='Select a date',
        validators=[validate_future_date]
    )

    start_time = forms.TimeField(widget=forms.TimeInput(format='%H:%M'),
                                 initial=datetime.now().time(),
                                 help_text='Format: HH:MM (e.g., 09:15)'
                                 )

    # Shop da se stava kako default
    def __init__(self, *args, **kwargs):
        self.shop = kwargs.pop('shop', None)
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
            if apt_date == date.today():
                # Dali start_time e vo idnina?
                if start_time < datetime.now().time():
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

            # Convert end_datetime to a datetime.time object
            end_time = end_datetime.time()

            print(f'opens={type(opens)}, start_time={type(start_time)}, end_time={type(end_time)}closes={type(closes)}')
            print(f'{opens}<{start_time}<{closes} = {opens < start_time < closes}')

            if not opens < end_time < closes and day_of_week in shop.working_week_days():
                self.add_error('start_time', "The end of the appointment is past the shop's closing time.")

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
