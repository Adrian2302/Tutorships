from django.urls import path
from . import views

urlpatterns = [
    path("estudiante", views.student_index, name="student"),
    path(r'estudiante/buscar', views.search_course, name="search"),
    path('estudiante/curso/<str:course_name>/agendar', views.request_tutorship, name="request_tutorship"),
    path('estudiante/curso/<str:course_name>', views.course_detail, name="course_detail"),
    path('estudiante/tutoria/pendientes', views.student_pending_request,
         name='student_pending_request'),
    path('estudiante/tutoria/aceptadas', views.student_accepted_request,
         name='student_accepted_request'),
    path('estudiante/tutoria/rechazadas', views.student_rejected_request,
         name='student_rejected_request'),
    path('estudiante/tutoria/historial', views.student_done_tutorship,
         name='student_done_request'),
    path('estudiante/tutoria/pendientes/<int:pk_request>', views.student_pending_request,
         name='student_pending_request'),
    path('estudiante/tutoria/aceptadas/<int:pk_request>', views.student_accepted_request,
         name='student_accepted_request'),
    path('estudiante/tutoria/rechazadas/<int:pk_request>', views.student_rejected_request,
         name='student_rejected_request'),
    path('estudiante/tutoria/historial/<int:pk_request>', views.student_done_tutorship,
         name='student_done_request')
]
    
