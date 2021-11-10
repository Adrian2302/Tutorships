from django.shortcuts import render
from . import forms
from .forms import ResourceForm
from .models import Resource
# noinspection PyUnresolvedReferences
from UserAuthentication.models import User


def add_resource(request):
    """This is the view for the add resource admin page."""
    user: User = User.objects.get(pk=request.user.id)

    if user.type == 3:
        form: ResourceForm = forms.ResourceForm(request.POST or None)

        if form.is_valid():
            resource: Resource = Resource(
                name=form.cleaned_data['name'],
                is_public=form.cleaned_data['is_public'],
                description=form.cleaned_data['description'],
                url=form.cleaned_data['url'],
                author=form.cleaned_data['author']
            )
            resource.save()

        context = {
            'form': form
        }
        return render(request, 'adminCrudForm.html', context)

    else:
        return render(request, 'UserAuthentication/index.html')
