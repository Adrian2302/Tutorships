from django.urls import path
from . import views

urlpatterns = [
    path('add_resource', views.add_resource, name="add_resource")
]
