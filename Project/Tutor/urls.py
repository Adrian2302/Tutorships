from django.urls import path, include
from django.contrib.auth.views import LogoutView
from django.views.generic.base import View
from . import views

urlpatterns = [
    path('calendario', views.CalendarView.as_view(), name='tutor_calendar'),
    path('perfil', views.ProfileView.as_view(), name='tutor_profile'),
    path('cursos', views.CourseView.as_view(), name='tutor_courses'),
]
