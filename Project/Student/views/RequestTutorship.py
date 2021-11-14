import datetime
from django.views import generic
from django.shortcuts import redirect, render

from Student.models import Request
from UserAuthentication.models import User
from Session.models import Session
from Modality.models import Modality
from Course.models import Course
from Tutorship.models import RequestNotification


def check_values_get(request):
    return request.GET.get('tutor') is not None \
           and request.GET.get('fecha') \
           and request.GET.get('sesion') is not None \
           and request.GET.get('modalidad') is not None \
           and request.GET.get('inicial') is not None \
           and request.GET.get('final') is not None


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
        tutorship_request = Request()

        tutorship_request.user_requester = User.objects.get(id=request.user.id)
        tutorship_request.tutor_requested = User.objects.get(email=request.GET.get('tutor'))
        tutorship_request.num_requesters = 1
        tutorship_request.tutor_comment = None

        if valid_comment(request.GET.get('comentario')):
            tutorship_request.student_comment = request.GET.get('comentario')
        else:
            tutorship_request.student_comment = None

        tutorship_request.session_requested = Session.objects.get(name=request.GET.get('sesion'))
        tutorship_request.modality_requested = Modality.objects.get(name=request.GET.get('modalidad'))
        tutorship_request.course_requested = Course.objects.get(course_name=course_name)

        start_date = datetime.datetime.strptime(request.GET.get('fecha'), "%d/%m/%Y")
        start_date_end_values = start_date.replace(hour=int(request.GET.get('inicial').split(":")[0]),
                                                   minute=int(request.GET.get('inicial').split(":")[1]))
        hour, minutes = get_added_hours(request.GET.get('final'))
        hours_added = datetime.timedelta(hours=hour, minutes=minutes)

        tutorship_request.date_start = start_date_end_values
        tutorship_request.date_end = start_date_end_values + hours_added
        tutorship_request.date_resolution = start_date_end_values

        tutorship_request.save()

        # add the notification here.
        notification = RequestNotification(
            notification_type='RE',
            to_user=tutorship_request.tutor_requested,
            from_user=tutorship_request.user_requester,
            request=tutorship_request
        )
        notification.save()

        return True
    except:
        return False


class RequestTutorship(generic.View):
    template_name = 'Student/reportRequest.html'

    def get(self, request, course_name):
        if request.user.is_authenticated:
            if check_values_get(request):
                success = request_maker(request, course_name)
                return render(request, self.template_name, {'success': success})
            return render(request, self.template_name, {'success': False})
        else:
            return redirect('index')
