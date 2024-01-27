from django import forms
from .models import WorkingTime


class WorkingTimeForm(forms.ModelForm):
    class Meta:
        model = WorkingTime
        fields = '__all__'

    opens = forms.TimeField(widget=forms.TimeInput(format='%H:%M'), initial='09:00',
                            help_text='Format: HH:MM (e.g., 09:15)')
    closes = forms.TimeField(widget=forms.TimeInput(format='%H:%M'), initial='23:00',
                             help_text='Format: HH:MM (e.g., 22:30)')
    day = forms.ChoiceField(
        choices=WorkingTime.WEEKDAYS,
        widget=forms.Select(attrs={'readonly': 'readonly'}),
    )


# Za sekoe ekstra pole da e avtomatski popolneto so den od nedelata
class WorkingTimeFormSet(forms.BaseInlineFormSet):

    def __init__(self, *args, **kwargs):
        super(WorkingTimeFormSet, self).__init__(*args, **kwargs)

        # denot se stava avtomatski
        for i in range(7):
            self.forms[i].initial['day'] = str(i + 1)