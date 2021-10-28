from django.urls import path
from . import views

urlpatterns = [
    path("student", views.student_index, name="student"),
    path(r'student/search', views.search_course, name="search"),
]
