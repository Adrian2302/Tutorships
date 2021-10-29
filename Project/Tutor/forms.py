from django.db.models import fields, query
from UserAuthentication.models import User
from . import models
from UserAuthentication.models import TutorCourse
from Payment.models import Payment
from Modality.models import Modality
from Session.models import Session
from Course.models import Course
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

class AddCourseForm(forms.Form):

    def __init__(self, *args, **kwargs):
        
        user = kwargs.pop('user')
        super(AddCourseForm, self).__init__(*args, **kwargs)
        
        user_courses = TutorCourse.objects.filter(user_id=user.id).values('course_id')

        if user_courses is not None and user_courses.count() > 0:
            not_added_courses = Course.objects.exclude(id__in = user_courses)
            self.fields['choices'].queryset = not_added_courses

    fields = ['course_name']

    choices = forms.ModelChoiceField(widget=forms.Select(
       attrs={'class': 'custom-select'}),
       queryset=Course.objects.all(),
       empty_label=None)
       
    choices.label = ''


    
