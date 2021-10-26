from . import models
from django import forms
from bootstrap_datepicker_plus import DatePickerInput
from bootstrap_datepicker_plus import TimePickerInput

class CreateTutorshipForm(forms.ModelForm):
    class Meta:
        model = models.Tutorship
        fields = [
            'max_people',
            'amount_per_person',
            'increment_per_half_hour'
        ]

        labels = {
            'max_people': 'Máximo de Personas',
            'amount_per_person': 'Precio',
            'increment_per_half_hour': 'Precio por 30 Minutos Extra'
        }

        widgets = {
            'max_people': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'required': 'true'}),
            'amount_per_person': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'required': 'true'}),
            'increment_per_half_hour': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'required': 'true'})
        }

class CreateTutorshipForm2(forms.ModelForm):
    class Meta:
        model = models.TutorshipAvailableSchedule
        fields = [
            'date',
            'start_hour',
            'end_hour'
        ]

        labels = {
            'date': 'Fecha',
            'start_hour': 'Hora de Inicio',
            'end_hour': 'Hora de Finalización'
        }

        widgets = {
            'date': DatePickerInput(format='%Y/%m/%d'),
            'start_hour': TimePickerInput().start_of('party time'),
            'end_hour': TimePickerInput().end_of('party time'),
        }
