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
from Student.models import Request
import datetime
# Create your views here.

def student_index(request):
    return render(request, 'Student/index.html')

def search_course(request): 
    search_query = request.GET.get('buscar')
    page_number = request.GET.get('pagina')

    if search_query=="all":
        results = Course.objects.all()
    else:
        if cache.get('latest_search') == search_query and cache.get('latest_results') is not None:
            results = cache.get('latest_results')
        else:
            results = Course.objects.filter(course_name__icontains=search_query)
            cache.set('latest_search', search_query)
        cache.set('latest_results', results)
    
    if search_query == None or search_query == "":
        redirect('index')
    
    paginator = Paginator(results, settings.PAGE_SIZE)
    page_display = paginator.get_page(page_number)
    sessions = Session.objects.all()
    modals = Modality.objects.all()
    
    context={
        'latest_search': search_query,
        'results': page_display,
        'sessions': sessions,
        'modals': modals
    }
    return render(request, "Student/search.html", context)

def get_context_view_calendar(tutor:User, course_name:str):

    course = Course.objects.get(course_name=course_name)
    tutors = TutorCourse.objects.filter(course_id = course).values("user")
    tutors_display = User.objects.filter(id__in=tutors)
    
    if tutor is None:
        tutor = tutors_display.first() 
    
    tutor_values= Tutor.objects.get(user=tutor)
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
    sessions = Session.objects.filter(id__in = Tutor.objects.filter(user=tutor).values("session_type"))
    modals = Modality.objects.filter(id__in = Tutor.objects.filter(user=tutor).values("modality_type"))
    context = {
        'tutors': tutors_display,
        'events': event_list,
        'calendar_title': tutor.name + " " + tutor.lastname,
        'sessions': sessions,
        'modals': modals,
        'course': course_name,
        'increment' : tutor_values.increment_per_half_hour,
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
    if request.GET.get('tutor') != None and request.GET.get('fecha') and request.GET.get('sesion') != None and request.GET.get('modalidad') != None and request.GET.get('inicial') != None and request.GET.get('final') != None:
        return True
    return False

def get_added_hours(added_hours):
    if added_hours == "1":
        return (1,30)
    elif added_hours == "2":
        return (2,0)
    return (1,0)

def valid_comment(comment: str):
    if comment is not None and comment.replace(" ","") != "":
        return True
    return False

def request_tutorship(request, course_name):
    if request.user.is_authenticated:
        print(request.method)
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
                start_date_end_values = start_date.replace(hour=int(request.GET.get('inicial').split(":")[0]), minute=int(request.GET.get('inicial').split(":")[1]))
                hour, minutes = get_added_hours(request.GET.get('final'))
                hours_added = datetime.timedelta(hours=hour , minutes= minutes)

                request_builder.date_start = start_date_end_values
                request_builder.date_end = start_date_end_values + hours_added
                request_builder.date_resolution = start_date_end_values

                request_builder.save()


                return render(request, "Student/reportRequest.html")

        return HttpResponse("error")