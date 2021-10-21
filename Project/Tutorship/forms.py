from . import models
from django import forms
from bootstrap_datepicker_plus import DatePickerInput
from bootstrap_datepicker_plus import TimePickerInput

class CreateTutorshipForm(forms.ModelForm):
    class Meta:
        model = models.Tutorship
        fields = [
            'maxPeople',
            'amountPerPerson',
            'incrementPerHalfHour',
            'typeSession',
            'typeMode'
        ]

        labels = {
            'maxPeople': 'Máximo de Personas',
            'amountPerPerson': 'Precio',
            'incrementPerHalfHour': 'Precio por 30 Minutos Extra',
            'typeSession': 'Tipo',
            'typeMode': 'Modalidad'
        }

        widgets = {
            'maxPeople': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'required': 'true'}),
            'amountPerPerson': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'required': 'true'}),
            'incrementPerHalfHour': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'required': 'true'}),
            'typeSession': forms.Select(choices=[('1', 'Individual'), ('2', 'Grupal')], attrs={'class': 'form-select'}),
            'typeMode': forms.Select(choices=[('1', 'Presencial'), ('2', 'Virtual')], attrs={'class': 'form-select'})
        }

class CreateTutorshipForm2(forms.ModelForm):
    class Meta:
        model = models.TutorshipAvailableSchedule
        fields = [
            'date',
            'startHour',
            'endHour'
        ]

        labels = {
            'date': 'Fecha',
            'startHour': 'Hora de Inicio',
            'endHour': 'Hora de Finalización'
        }

        widgets = {
            'date': DatePickerInput(format='%m/%d/%Y'),
            'startHour': TimePickerInput().start_of('party time'),
            'endHour': TimePickerInput().end_of('party time'),
        }
