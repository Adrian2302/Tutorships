from django.shortcuts import redirect, render
from django.shortcuts import HttpResponse
from . import models
from . import forms

# Create your views here.
from .forms import NewAdminForm
from .models import User


def index(request):
    if models.User.objects.filter(pk=request.user.id).exists():

        user: User = models.User.objects.get(pk=request.user.id)

        if user.type == 3:
            return render(request, "UserAuthentication/adminLogin.html")

        return HttpResponse("Hello")
    else:
        return render(request, "Student/index.html")
    

def login(request):
    if models.User.objects.filter(pk=request.user.id).exists():
        print("ee")
        return redirect('index')
    else:
        form = forms.UserForm(request.POST or None)

        if form.is_valid():
            user = models.User(id=request.user.id, email=request.user.email,
                               name=form.cleaned_data['name'], lastname=form.cleaned_data['lastname'],
                               type=form.cleaned_data['type'])
            user.save()
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
