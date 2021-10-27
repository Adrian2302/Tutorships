from django.urls import path, include
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('create_tutorship', views.tutor_create_tutorship),
    path('calendario', views.CalendarView.as_view(), name='tutor_calendar'),
]