from django.urls import path
from . import views

urlpatterns = [
    path("estudiante", views.student_index, name="student"),
    path(r'estudiante/buscar', views.search_course, name="search"),
]
