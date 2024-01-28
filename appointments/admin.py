from django.contrib import admin
from .models import Appointment
from .forms import AppointmentForm


class AppointmentAdmin(admin.ModelAdmin):
    model = Appointment
    form = AppointmentForm
    list_display = ('code', 'shop', 'formatted_date', 'formatted_start_time', 'formatted_end_time', 'total_price', 'user')
    readonly_fields = ('duration', 'shop', 'user', 'total_price', 'code')
    ordering = ('date', 'start_time')

    def formatted_date(self, obj):
        return obj.date.strftime('%d/%m/%Y')

    def formatted_start_time(self, obj):
        return obj.start_time.strftime('%H:%M')

    def formatted_end_time(self, obj):
        return obj.end_time.strftime('%H:%M')

    formatted_date.short_description = 'Date'
    formatted_start_time.short_description = 'Start Time'
    formatted_end_time.short_description = 'End Time'


admin.site.register(Appointment, AppointmentAdmin)
