from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.core.cache import cache
from django.core.paginator import Paginator
from django.conf import settings
from Course.models import Course
from Session.models import Session
from Modality.models import Modality
from UserAuthentication.models import TutorCourse, User
from Tutor.models import TutorAvailableSchedule, Tutor
from Tutorship.models import Tutorship, TutorshipScore
from Student.models import Request
import datetime


def student_index(request):
    return render(request, 'Student/index.html')


def search_course(request):
    search_query = request.GET.get('buscar')
    page_number = request.GET.get('pagina')

    if search_query == "all":
        results = Course.objects.all()
    else:
        if cache.get('latest_search') == search_query and cache.get('latest_results') is not None:
            results = cache.get('latest_results')
        else:
            results = Course.objects.filter(course_name__icontains=search_query)
            cache.set('latest_search', search_query)
        cache.set('latest_results', results)

    if search_query is None or search_query == "":
        redirect('index')

    paginator = Paginator(results, settings.PAGE_SIZE)
    page_display = paginator.get_page(page_number)
    sessions = Session.objects.all()
    modals = Modality.objects.all()

    context = {
        'latest_search': search_query,
        'results': page_display,
        'sessions': sessions,
        'modals': modals
    }
    return render(request, "Student/search.html", context)


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


def course_detail(request, course_name):
    if request.user.is_authenticated:
        user = None
        if request.method == 'POST':
            user = User.objects.get(email=request.POST.get('tutor'))
        context = get_context_view_calendar(user, course_name)
        return render(request, "Student/courseDetail.html", context)
    else:
        return redirect('index')


def check_values_get(request):
    if request.GET.get('tutor') is not None and request.GET.get('fecha') and request.GET.get(
            'sesion') is not None and request.GET.get('modalidad') is not None and request.GET.get(
        'inicial') is not None and request.GET.get('final') is not None:
        return True
    return False


def get_added_hours(added_hours):
    if added_hours == "1":
        return 1, 30
    elif added_hours == "2":
        return 2, 0
    return 1, 0


def valid_comment(comment: str):
    if comment is not None and comment.replace(" ", "") != "":
        return True
    return False


def request_tutorship(request, course_name):
    if request.user.is_authenticated:
        if request.method == 'GET':
            if check_values_get(request):
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

                return render(request, "Student/reportRequest.html", {'success': True})

        return render(request, "Student/reportRequest.html", {'success': False})
    else:
        return redirect('index')


def student_pending_request(request):
    user = User.objects.get(pk=request.user.id)
    if user.is_student():
        query_set = list(Request.objects.filter(user_requester=user, state='PN').order_by('date_start'))
        context = {'requests': query_set}
        return render(request, "Student/studentRequest.html", context)
    else:
        return redirect('index')


def student_accepted_request(request):
    user = User.objects.get(pk=request.user.id)
    if user.is_student():
        query_set = list(Request.objects.filter(user_requester=user, state='AP').order_by('date_start'))
        context = {'requests': query_set}
        return render(request, "Student/studentRequest.html", context)
    else:
        return redirect('index')


def student_rejected_request(request):
    user = User.objects.get(pk=request.user.id)
    if user.is_student():
        query_set = list(Request.objects.filter(user_requester=user, state='DD').order_by('date_start'))
        context = {'requests': query_set}
        return render(request, "Student/studentRequest.html", context)
    else:
        return redirect('index')


def student_done_tutorship(request):
    user = User.objects.get(pk=request.user.id)
    if user.is_student():
        if request.method == 'POST':
            id_request = request.POST.get('tutorship')
            score = request.POST.get('score_options')
            tutorship = Tutorship.objects.get(pk=id_request)

            tutorship_score = TutorshipScore(
                tutorship=tutorship,
                score=score,
            )
            tutorship_score.save()
            return redirect('student_done_request')

        query_set = list(Tutorship.objects.filter(state='DN')
                         .select_related('request')
                         .filter(request__user_requester=user))
        context = {'tutorships': query_set}
        return render(request, "Student/studentHistory.html", context)
    else:
        return redirect('index')
