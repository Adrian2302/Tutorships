from django.views import generic
from django.core.cache import cache
from django.shortcuts import redirect, render

from UserAuthentication.models import User, TutorCourse
from Course.models import Course
from Tutor.models import Tutor, TutorAvailableSchedule
from Session.models import Session
from Modality.models import Modality

def get_context_view_calendar(tutor: User, course_name: str):
    course = Course.objects.get(course_name=course_name)
    tutors = TutorCourse.objects.filter(course_id=course).values("user")
    tutors_display = User.objects.filter(id__in=tutors)

    if tutor is None:
        tutor = tutors_display.first()

    tutor_values = Tutor.objects.get(user=tutor)
    cache.set('tutor', tutor)
    events = TutorAvailableSchedule.objects.filter(
        user=tutor
    ).order_by('start_time')
    event_list = []
    for event in events:
        event_list.append(
            {
                'message': event.start_time.strftime("%H:%M") + " - " + event.end_time.strftime("%H:%M"),
                'start': event.start_time.strftime("%Y-%m-%d %H:%M"),
                'end': event.end_time.strftime("%Y-%m-%d %H:%M"),
            }
        )
    sessions = Session.objects.filter(id__in=Tutor.objects.filter(user=tutor).values("session_type"))
    modals = Modality.objects.filter(id__in=Tutor.objects.filter(user=tutor).values("modality_type"))
    context = {
        'tutors': tutors_display,
        'events': event_list,
        'calendar_title': tutor.name + " " + tutor.lastname,
        'sessions': sessions,
        'modals': modals,
        'course': course_name,
        'increment': tutor_values.increment_per_half_hour,
        'value_tutorship': tutor_values.amount_per_person,
        'email_selected_tutor': tutor.email
    }

    return context

class displayCourseDetail(generic.View):

    def get(self, request, course_name):
        if request.user.is_authenticated:
            context = get_context_view_calendar(None, course_name)
            return render(request, "Student/courseDetail.html", context)
        else:
            return redirect('index')

    def post(self, request, course_name):
        if request.user.is_authenticated:
            requested_tutor = User.objects.get(email=request.POST.get('tutor'))
            context = get_context_view_calendar(requested_tutor, course_name)
            return render(request, "Student/courseDetail.html", context)
        else:
            return redirect('index')