from . import models
from django import forms


class add_course_form(forms.ModelForm):
    class Meta:
        model = models.Course
        fields = [
            'university',
            'course_name',
            'description'
        ]

        labels = {
            'university': 'Universidad',
            'course_name': 'Nombre del curso',
            'description': 'Descripción del curso'
        }

        widgets = {
            'university': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'course_name': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'})
        }
