from django.urls import path, include
from django.contrib.auth.views import LogoutView
from django.views.generic.base import View
from . import views

urlpatterns = [
    path('calendario', views.CalendarView.as_view(), name='tutor_calendar'),
    path('perfil', views.ProfileView.as_view(), name='tutor_profile'),
    path('cursos', views.CourseView.as_view(), name='tutor_courses'),
    path('pendientes', views.PendingRequestView.as_view(), name='tutor_pending_requests'),
    path(r'pendientes/<int:request_pk>', views.PendingRequestView.as_view(), name='tutor_pending_requests'),
    path('aceptadas', views.AcceptedRequestView.as_view(), name='tutor_accepted_requests'),
    path(r'aceptadas/<int:request_pk>', views.AcceptedRequestView.as_view(), name='tutor_accepted_requests'),
]
