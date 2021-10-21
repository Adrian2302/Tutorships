from django.urls import path
from . import views

urlpatterns = [
    path('add_payment', views.add_payment, name="add_payment")
]
