from django.shortcuts import render
from . import forms
from .forms import AddModalityForm
from .models import Modality
# noinspection PyUnresolvedReferences
from UserAuthentication.models import User


def add_modality(request):
    """This is the view for the add modality admin page."""
    user: User = User.objects.get(pk=request.user.id)

    if user.is_admin():
        form: AddModalityForm = forms.AddModalityForm(request.POST or None)

        if form.is_valid():
            modality: Modality = Modality(
                name=form.cleaned_data['name'],
                description=form.cleaned_data['description'],
            )
            modality.save()

        context = {
            'form': form
        }
        return render(request, 'adminCrudForm.html', context)

    else:
        return render(request, 'UserAuthentication/index.html')
