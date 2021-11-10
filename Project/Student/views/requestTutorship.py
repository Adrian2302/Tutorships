import datetime
from django.views import generic
from django.shortcuts import redirect, render

from Student.models import Request
from UserAuthentication.models import User
from Session.models import Session
from Modality.models import Modality
from Course.models import Course

def check_values_get(request):
    if request.GET.get('tutor') is not None and request.GET.get('fecha') and request.GET.get(
            'sesion') is not None and request.GET.get('modalidad') is not None and request.GET.get(
        'inicial') is not None and request.GET.get('final') is not None:
        return True
    return False

def valid_comment(comment: str):
    if comment is not None and comment.replace(" ", "") != "":
        return True
    return False

def get_added_hours(added_hours):
    if added_hours == "1":
        return 1, 30
    elif added_hours == "2":
        return 2, 0
    return 1, 0

def request_maker(request, course_name):
    try:
        request_builder = Request()

        request_builder.user_requester = User.objects.get(id=request.user.id)
        request_builder.tutor_requested = User.objects.get(email=request.GET.get('tutor'))
        request_builder.num_requesters = 1
        request_builder.tutor_comment = None

        if valid_comment(request.GET.get('comentario')):
            request_builder.student_comment = request.GET.get('comentario')
        else:
            request_builder.student_comment = None

        request_builder.session_requested = Session.objects.get(name=request.GET.get('sesion'))
        request_builder.modality_requested = Modality.objects.get(name=request.GET.get('modalidad'))
        request_builder.course_requested = Course.objects.get(course_name=course_name)

        start_date = datetime.datetime.strptime(request.GET.get('fecha'), "%d/%m/%Y")
        start_date_end_values = start_date.replace(hour=int(request.GET.get('inicial').split(":")[0]),
                                                minute=int(request.GET.get('inicial').split(":")[1]))
        hour, minutes = get_added_hours(request.GET.get('final'))
        hours_added = datetime.timedelta(hours=hour, minutes=minutes)

        request_builder.date_start = start_date_end_values
        request_builder.date_end = start_date_end_values + hours_added
        request_builder.date_resolution = start_date_end_values

        request_builder.save()

        return True
    except:
        return False

class requestTutorship(generic.View):

    def get(self, request, course_name):
        if request.user.is_authenticated:
            if check_values_get(request):
                success = request_maker(request, course_name)
                return render(request, "Student/reportRequest.html", {'success': success})

            return render(request, "Student/reportRequest.html", {'success': False})
        else:
            return redirect('index')