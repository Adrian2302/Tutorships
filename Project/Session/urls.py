from django.urls import path
from . import views

urlpatterns = [
    path('add_session', views.add_session, name="add_session")
]
