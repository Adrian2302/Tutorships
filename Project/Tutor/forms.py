from . import models
from UserAuthentication.models import TutorCourse
from Payment.models import Payment
from Modality.models import Modality
from Session.models import Session
from Tutor.models import Tutor
from django import forms
from bootstrap_datepicker_plus import DateTimePickerInput


class TutorScheduleForm(forms.ModelForm):
    class Meta:
        model = models.TutorAvailableSchedule
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

    tutorship_price = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control'}),
        initial=None)
    increment_half_hour = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control'}),
        initial=None)

    tutorship_price.label = "Indique su precio de las tutorías"
    increment_half_hour.label = "Indique su precio por el incremento de media hora"

    def __init__(self, *args, **kwargs):
        if kwargs.get('user'):
            user = kwargs.pop('user')
            tutorship_price = Tutor.objects.get(user_id=user.id).amount_per_person
            increment_half_hour = Tutor.objects.get(user_id=user.id).increment_per_half_hour
            super(ProfileForm, self).__init__(*args, **kwargs)
            self.fields['tutorship_price'].initial = tutorship_price
            self.fields['increment_half_hour'].initial = increment_half_hour
        else:
            super(ProfileForm, self).__init__(*args, **kwargs)


class ProfileSessionForm(forms.Form):
    choices_session = forms.ModelChoiceField(widget=forms.RadioSelect(
        attrs={'class': 'form-check-input',
               'id': 'session_choices'}),
        queryset=Session.objects.all(),
        empty_label=None,
        initial=None)

    choices_session.label = "Seleccione el tipo de sesión a impartir"

    def __init__(self, *args, **kwargs):
        if kwargs.get('user'):
            user = kwargs.pop('user')
            session = Tutor.objects.get(user_id=user.id).session_type_id
            super(ProfileSessionForm, self).__init__(*args, **kwargs)
            self.fields['choices_session'].initial = session
        else:
            super(ProfileSessionForm, self).__init__(*args, **kwargs)


class ProfileModalityForm(forms.Form):

    choices_modality = forms.ModelChoiceField(widget=forms.RadioSelect(
        attrs={'class': 'form-check-input',
               'id': 'modality_choices'}),
        queryset=Modality.objects.all(),
        empty_label=None,
        initial=None)

    choices_modality.label = "Seleccione una el tipo de modalidad a impartir"

    def __init__(self, *args, **kwargs):
        if kwargs.get('user'):
            user = kwargs.pop('user')
            modality = Tutor.objects.get(user_id=user.id).modality_type_id
            super(ProfileModalityForm, self).__init__(*args, **kwargs)
            self.fields['choices_modality'].initial = modality
        else:
            super(ProfileModalityForm, self).__init__(*args, **kwargs)


class ProfilePaymentForm(forms.Form):
    choices_payment = forms.ModelChoiceField(widget=forms.RadioSelect(
        attrs={'class': 'form-check-input',
               'id': 'payment_choices',
               'name': 'payment_choices'}),
        queryset=Payment.objects.all(),
        empty_label=None,
    )

    choices_payment.label = "Seleccione un método de pago"

    def __init__(self, *args, **kwargs):
        if kwargs.get('user'):
            user = kwargs.pop('user')
            payment = Tutor.objects.get(user_id=user.id).payment_type_id
            super(ProfilePaymentForm, self).__init__(*args, **kwargs)
            self.fields['choices_payment'].initial = payment
        else:
            super(ProfilePaymentForm, self).__init__(*args, **kwargs)

