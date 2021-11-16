from django.db.models import fields, query
from UserAuthentication.models import User
from . import models
from Tutor.models import TutorCourse
from Payment.models import Payment
from Modality.models import Modality
from Session.models import Session
from Tutor.models import Tutor
from Course.models import Course
from django import forms
from bootstrap_datepicker_plus import DateTimePickerInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Div
from crispy_forms.bootstrap import PrependedText

import datetime



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
    tutorship_price = forms.CharField(widget=forms.TextInput,
                                      initial=None,
                                      label="Precio de mis tutorías:")

    increment_half_hour = forms.CharField(widget=forms.TextInput,
                                          initial=None,
                                          label="Precio por el incremento de media hora:")

    choices_session = forms.ModelChoiceField(widget=forms.RadioSelect,
                                             queryset=Session.objects.all(),
                                             initial=None,
                                             label="Tipo de sesión a impartir:")

    choices_modality = forms.ModelChoiceField(widget=forms.RadioSelect,
                                              queryset=Modality.objects.all(),
                                              initial=None,
                                              label="Tipo de modalidad a impartir:")

    choices_payment = forms.ModelChoiceField(widget=forms.RadioSelect,
                                             queryset=Payment.objects.all(),
                                             initial=None,
                                             label="Método de pago preferido:")

    helper = FormHelper()
    helper.use_custom_control = False
    helper.form_class = 'blueForms'
    helper.layout = Layout(
        Div(PrependedText('tutorship_price', '₡', css_class='form-control'),
            css_class='input-group-prepend'),
        Div(PrependedText('increment_half_hour', '₡', css_class='form-control'),
            css_class='input-group-prepend'),
        Field('choices_session'),
        Field('choices_modality'),
        Field('choices_payment'),
        Submit('submit', 'Guardar', css_class='btn btn-primary'),
    )

    def __init__(self, *args, **kwargs):
        if kwargs.get('user'):
            user = kwargs.pop('user')
            tutorship_price = Tutor.objects.get(user_id=user.id).amount_per_person
            increment_half_hour = Tutor.objects.get(user_id=user.id).increment_per_half_hour
            session = Tutor.objects.get(user_id=user.id).session_type_id
            modality = Tutor.objects.get(user_id=user.id).modality_type_id
            payment = Tutor.objects.get(user_id=user.id).payment_type_id

            super(ProfileForm, self).__init__(*args, **kwargs)

            self.fields['tutorship_price'].initial = tutorship_price
            self.fields['increment_half_hour'].initial = increment_half_hour
            self.fields['choices_session'].initial = session
            self.fields['choices_modality'].initial = modality
            self.fields['choices_payment'].initial = payment

        else:
            super(ProfileForm, self).__init__(*args, **kwargs)


class AddCourseForm(forms.Form):

    def __init__(self, *args, **kwargs):
        if kwargs.get('user'):
            user = kwargs.pop('user')
            super(AddCourseForm, self).__init__(*args, **kwargs)

            user_courses = TutorCourse.objects.filter(user_id=user.id).values('course_id')

            if user_courses is not None and user_courses.count() > 0:
                not_added_courses = Course.objects.exclude(id__in=user_courses)
                self.fields['choices'].queryset = not_added_courses
        else:
            super(AddCourseForm, self).__init__(*args, **kwargs)

    fields = ['course_name']

    choices = forms.ModelChoiceField(widget=forms.Select(
        attrs={'class': 'custom-select'}),
        queryset=Course.objects.all(),
        empty_label=None)

    choices.label = ''
