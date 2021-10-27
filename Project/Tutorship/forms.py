from . import models
from django import forms
from bootstrap_datepicker_plus import DateTimePickerInput


class TutorshipForm(forms.ModelForm):
    class Meta:
        model = models.TutorshipAvailableSchedule
        fields = ['start_time', 'end_time']
        labels = {
            'start_time': 'Inicio del bloque',
            'end_time': 'Fin del bloque'
        }
        widgets = {
            'start_time': DateTimePickerInput(
                format='%Y-%m-%d %H:%M',
                options={
                    'locale': 'es',
                    'stepping': '30'
                }
            ).start_of('block'),
            'end_time': DateTimePickerInput(
                format='%Y-%m-%d %H:%M',
                options={
                    'locale': 'es',
                    'stepping': '30'
                }
            ).end_of('block'),
        }
