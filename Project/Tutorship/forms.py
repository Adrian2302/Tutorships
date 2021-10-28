from . import models
from UserAuthentication.models import TutorCourse
from Payment.models import Payment
from Modality.models import Modality
from Session.models import Session
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


class ProfileForm(forms.Form):
    # registered_courses = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    # registered_courses.label = "Cursos registrados"

    tutorship_price = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    increment_half_hour = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    tutorship_price.label = "Precio de las tutorías"
    increment_half_hour.label = "Precio por incremento de media hora"


class ProfileModalityForm(forms.Form):
    choices = forms.ModelChoiceField(widget=forms.CheckboxSelectMultiple(
        attrs={'class': 'form-check-input'}),
        queryset=Modality.objects.all(),
        empty_label=None)

    choices.label = "Modalidades a impartir"


class ProfileSessionForm(forms.Form):
    choices = forms.ModelChoiceField(widget=forms.CheckboxSelectMultiple(
        attrs={'class': 'form-check-input'}),
        queryset=Session.objects.all(),
        empty_label=None)

    choices.label = "Sesiones a impartir"


class ProfilePaymentForm(forms.Form):
    choices = forms.ModelChoiceField(widget=forms.CheckboxSelectMultiple(
        attrs={'class': 'form-check-input'}),
        queryset=Payment.objects.all(),
        empty_label=None)

    choices.label = "Métodos de pago"
