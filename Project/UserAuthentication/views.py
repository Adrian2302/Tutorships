import json
from django.shortcuts import render
from django.shortcuts import HttpResponse
from . import models

# Create your views here.

def index(request):
    return render(request, "UserAuthentication/index.html")

def login(request):
    user = models.User(id = request.user.id, name = request.user.username, email = request.user.email, 
        lastname = request.user.username, type = 1, photo_profile = "test")
    user.save()
    return HttpResponse("Hello")