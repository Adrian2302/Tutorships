from django.urls import path, include
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('create-Tutorship', views.tutor_create_tutorship),
    
]