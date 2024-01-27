from django import forms
from .models import Service


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = '__all__'

    time_to_complete = forms.TimeField(widget=forms.TimeInput(format='%H:%M'),
                                       initial='00:15',
                                       help_text='Format: HH:MM (e.g., 00:25)')
