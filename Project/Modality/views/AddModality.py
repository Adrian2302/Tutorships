from django.shortcuts import render, redirect
from Modality import models
from Modality.forms import AddModalityForm
from django.views import generic
# noinspection PyUnresolvedReferences
from UserAuthentication.models import User


def create_context(form):
    return {'form': form}

class AddModality(generic.View):
    """This is the view for the add modality admin page."""
    def get(self, request):

        user: User = User.objects.get(pk=request.user.id)

        if user.is_admin():
            form = AddModalityForm
            context = create_context(form)

            return render(request, 'adminCrudForm.html', context)

        else:
            return redirect('index')

    def post(self, request):

        user: User = User.objects.get(pk=request.user.id)

        if user.is_admin():
            form: AddModalityForm = AddModalityForm(request.POST or None)

            if form.is_valid():
                modality: models.Modality = models.Modality(
                    name=form.cleaned_data['name'],
                    description=form.cleaned_data['description'],
                )
                modality.save()
            
            context = create_context(form)

            return render(request, 'adminCrudForm.html', context)

        else:
            return render(request, 'UserAuthentication/index.html')