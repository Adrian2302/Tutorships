from django.shortcuts import render
from . import forms
from .forms import AddSessionForm
from .models import Session
# noinspection PyUnresolvedReferences
from UserAuthentication.models import User


def add_session(request):
    """This is the view for the add session admin page."""
    user: User = User.objects.get(pk=request.user.id)

    if user.is_admin():
        form: AddSessionForm = forms.AddSessionForm(request.POST or None)

        if form.is_valid():
            session: Session = Session(
                name=form.cleaned_data['name'],
                description=form.cleaned_data['description'],
            )
            session.save()

        context = {
            'form': form
        }
        return render(request, 'adminCrudForm.html', context)

    else:
        return render(request, 'UserAuthentication/index.html')
