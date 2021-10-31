from django.urls import path
from . import views

urlpatterns = [
    path("estudiante", views.student_index, name="student"),
    path(r'estudiante/buscar', views.search_course, name="search"),
    path('estudiante/curso/<str:course_name>/agendar', views.request_tutorship, name="request_tutorship"),
    path('estudiante/curso/<str:course_name>', views.course_detail, name="course_detail"),
]
    
