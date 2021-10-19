import json
from django.shortcuts import render
from django.shortcuts import HttpResponse
from . import models

# Create your views here.

def index(request):
    return render(request, "UserAuthentication/index.html")

def login(request):
    if models.User.objects.filter(pk = request.user.id).exists():
        return HttpResponse("Hello")
    else:
        context = {}
        context["email"] = request.user.email
        return render(request, "UserAuthentication/register.html", context)