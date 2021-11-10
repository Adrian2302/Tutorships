from django.shortcuts import redirect, render
from django.shortcuts import HttpResponse
from . import models
from . import forms
from .forms import NewAdminForm
from .models import User
from Tutor.models import Tutor


def index(request):
    if models.User.objects.filter(pk=request.user.id).exists():
        user: User = models.User.objects.get(pk=request.user.id)
        if user.is_tutor():
            return render(request, "UserAuthentication/tutorLogin.html")
        elif user.is_admin():
            return render(request, "UserAuthentication/adminLogin.html")
    return render(request, "Student/index.html")


def login(request):
    if models.User.objects.filter(pk=request.user.id).exists():
        return redirect('index')
    else:
        form = forms.UserForm(request.POST or None)
        if form.is_valid():
            user = models.User(id=request.user.id, email=request.user.email,
                               name=form.cleaned_data['name'], lastname=form.cleaned_data['lastname'],
                               type=form.cleaned_data['type'])
            user.save()
            if user.is_tutor():
                tutor = Tutor(user=user)
                tutor.save()
        context = {
            'form': form,
            'email': request.user.email
        }
        return render(request, "UserAuthentication/register.html", context)


def add_administrator(request):
    """This is the view for the admin manager."""
    user: User = models.User.objects.get(pk=request.user.id)
    if user.type == 3:
        form: NewAdminForm = forms.NewAdminForm(request.POST or None)
        if form.is_valid():
            try:
                user: User = models.User.objects.get(email=form.cleaned_data['email'])
                user.type = 3
                user.save()
            except User.DoesNotExist:
                pass
        context = {
            'form': form
        }
        return render(request, 'adminCrudForm.html', context)
    else:
        return render(request, 'UserAuthentication/index.html')
