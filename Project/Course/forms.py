from . import models
from django import forms


class AddCourseForm(forms.ModelForm):
    class Meta:
        model = models.Course
        fields = [
            'university',
            'name',
            'description'
        ]

        labels = {
            'university': 'Universidad',
            'name': 'Nombre del curso',
            'description': 'Descripción del curso'
        }

        widgets = {
            'university': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'})
        }
