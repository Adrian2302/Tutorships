
from django.shortcuts import render
from django.shortcuts import HttpResponse
from . import models
from . import forms
# Create your views here.

def index(request):
    return render(request, "UserAuthentication/index.html")

def login(request):
    if models.User.objects.filter(pk = request.user.id).exists():
        return HttpResponse("Hello")
    else:
        form = forms.UserForm(request.POST or None)

        if form.is_valid():
            user = models.User(id = request.user.id, email = request.user.email, 
                name = form.cleaned_data['name'], lastname = form.cleaned_data['lastname'], type = form.cleaned_data['type'])
            user.save()
        context = {
            'form': form,
            'email': request.user.email
        }

        return render(request, "UserAuthentication/register.html", context)