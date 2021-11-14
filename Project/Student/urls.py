from django.urls import path
from . import views

urlpatterns = [
     path("estudiante", views.mainScreen.as_view(), name="index_student"),
     path(r'estudiante/buscar', views.searchCourse.as_view(), name="search"),
     path('estudiante/curso/<str:course_name>', views.displayCourseDetail.as_view(), name="course_detail"),
     path('estudiante/curso/<str:course_name>/agendar', views.RequestTutorship.as_view(), name="request_tutorship"),

     path('estudiante/tutoria/pendientes', views.pendingRequests.as_view(), name='student_pending_request'),
     path('estudiante/tutoria/aceptadas', views.acceptedRequests.as_view(), name='student_accepted_request'),
     path('estudiante/tutoria/rechazadas', views.rejectedRequests.as_view(), name='student_rejected_request'),
     path('estudiante/tutoria/historial', views.doneTutorships.as_view(), name='student_done_request'),

     path('estudiante/tutoria/pendientes/<int:pk_request>',
          views.pendingRequests.as_view(), name='student_pending_request'),
     path('estudiante/tutoria/aceptadas/<int:pk_request>',
          views.acceptedRequests.as_view(), name='student_accepted_request'),
     path('estudiante/tutoria/rechazadas/<int:pk_request>',
          views.rejectedRequests.as_view(), name='student_rejected_request'),
     path('estudiante/tutoria/historial/<int:pk_request>',
          views.doneTutorships.as_view(), name='student_done_request')
]
    
