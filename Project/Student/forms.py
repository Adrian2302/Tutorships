from . import models
from django import forms
from UserAuthentication.models import User

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'name',
            'lastname',
            'photo_profile'
        ]

        labels = {
            'name': 'Nombre',
            'lastname': 'Apellido',
            'photo_profile': 'Foto de perfil'
        }

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'lastname': forms.TextInput(attrs={'class': 'form-control'}),
            'photo_profile': forms.FileInput()
        }