from django.contrib import admin
from .models import Appointment
from .forms import AppointmentForm


class AppointmentAdmin(admin.ModelAdmin):
    model = Appointment
    form = AppointmentForm
    list_display = ('shop', 'date', 'start_time', 'end_time', 'total_price', 'user')
    readonly_fields = ('duration', 'shop', 'user', 'total_price')


admin.site.register(Appointment, AppointmentAdmin)
