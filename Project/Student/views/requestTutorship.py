from datetime import datetime, timedelta
from django.views import generic
from django.shortcuts import redirect, render
from django.core.cache import cache

from Student.models import Request, Requesters
from UserAuthentication.models import User
from Session.models import Session
from Modality.models import Modality
from Course.models import Course
from Tutor.models import TutorAvailableSchedule, Tutor
from Payment.models import Payment

instance_id = None

def save_values_post(request):
    dict_values = {}

    dict_values['user_requester'] = request.user

    if request.POST.get('fecha'):
        dict_values['fecha'] = request.POST.get('fecha')

    if request.POST.get('tutor'):
        dict_values['tutor'] = request.POST.get('tutor')
    
    if request.POST.get('sesion'):
        dict_values['sesion'] = request.POST.get('sesion')

    if request.POST.get('modalidad'):
        dict_values['modalidad'] = request.POST.get('modalidad')

    if request.POST.get('inicial'):
        dict_values['inicial'] = request.POST.get('inicial')

    if request.POST.get('final'):
        dict_values['final'] = get_added_hours(request.POST.get('final'))

    if request.POST.getlist('invitados'):
        dict_values['invitados'] = request.POST.getlist('invitados')

    if valid_comment(request.POST.get('comentario')):
        dict_values['comentario'] = request.POST.get('comentario')

    return dict_values

def check_dict_value(dict_values):
    valid_keys = ('tutor', 'sesion', 'modalidad', 'inicial', 'final', 'fecha')
    return all(key in dict_values for key in valid_keys)

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

def set_all_guests_request(dict_values, request_tutorship):
    for guest in dict_values['invitados']:
        print(guest)
        resquester = Requesters()
        resquester.request = request_tutorship
        resquester.user_requester = User.objects.get(id=guest)
        resquester.save()

def check_guests(dict_values):
    if dict_values['sesion'] == "Grupal - Privada":
        if 'invitados' in dict_values:
            return True
        else:
            raise Exception("No se han seleccionado invitados en una Grupal - Privada")
    return False

def request_maker(dict_values, course_name):
    try:
        schedule_selected = cache.get('schedule_selected')

        user_requester = User.objects.get(id=dict_values['user_requester'].id)
        tutor_requested = User.objects.get(id=dict_values['tutor'])

        num_requesters = 1
        
        session_requested = Session.objects.get(name=dict_values['sesion'])
        modality_requested = Modality.objects.get(name=dict_values['modalidad'])
        course_requested = Course.objects.get(course_name=course_name)

        start_date = datetime.strptime(dict_values['fecha'], "%Y-%m-%d")
        initial_hour, initial_minutes = dict_values['inicial'].split(":")

        start_date = start_date.replace(hour=int(initial_hour), minute=int(initial_minutes))

        final_hour, final_minutes = dict_values['final']
        time_added = timedelta(hours=final_hour, minutes=final_minutes)

        end_date = start_date + time_added
        
        do_requesters = check_guests(dict_values)
            
        request_builder = Request.objects.create(user_requester=user_requester,
                                                 tutor_requested=tutor_requested,
                                                 num_requesters=num_requesters,
                                                 session_requested=session_requested,
                                                 modality_requested=modality_requested,
                                                 course_requested=course_requested,
                                                 date_start=start_date,
                                                 date_end=end_date,
                                                 date_request=start_date)

        if 'comentario' in dict_values:
           request_builder.student_comment = dict_values['comentario']

        request_builder.save()

        print(request_builder.id)
        if do_requesters:
            set_all_guests_request(dict_values, request_builder)
        
    except Exception as e:
        print(e)
        raise Exception("Unknown exception")

def create_context(schedule_id, user):
    try:
        context = {}
        schedule_selected = TutorAvailableSchedule.objects.get(id=schedule_id)

        cache.set('schedule_selected', schedule_selected)
        tutor = Tutor.objects.get(user = schedule_selected.user)
        all_students = User.objects.filter(type=1).exclude(id=user.id).order_by('name')

        #Para la integración de varias sesiones se debe tener una lista de sesiones id y hacer id__in
        sessions = Session.objects.filter(id=tutor.session_type.id)
        modals = Modality.objects.filter(id=tutor.modality_type.id)
        payments = Payment.objects.filter(id=tutor.payment_type.id)
       
        min_time = schedule_selected.start_time.strftime('%H:%M')
        max_time = schedule_selected.end_time - timedelta(hours=1, minutes=0)
        max_time = max_time.strftime('%H:%M')

        context.update({
            'tutor': tutor,
            'students': all_students,
            'sessions': sessions,
            'modals': modals,
            'payments': payments,
            'min_time': min_time,
            'max_time': max_time,
            'value_tutorship_person': tutor.amount_per_person,
            'increment': tutor.increment_per_half_hour,
            'date':str(schedule_selected.start_time.date()),
            'students':all_students
        })

        return context  
    except schedule_selected.DoesNotExist:
        raise Exception("Schedule selected id is not in the database")
    except Exception as e:
        print(e)
        raise Exception("Unknown exception")

class requestTutorship(generic.View):

    def get(self, request, course_name):
        user= User.objects.get(id=request.user.id)
        if request.user.is_authenticated and user.is_student():
            try:            
                schedule_id = request.GET.get('schedule_number')
                context = create_context(schedule_id, user)
                return render(request, "Student/formRequestTutorship.html", context)
            except Exception as e:
                print(e)
        return redirect('index')

    def post(self, request, course_name):
        user= User.objects.get(id=request.user.id)
        if request.user.is_authenticated and user.is_student():
            try:
                dict_values = save_values_post(request)

                if check_dict_value(dict_values):          
                    request_maker(dict_values, course_name)
                    return render(request, "Student/reportRequest.html", {'success': True})
                return render(request, "Student/reportRequest.html", {'success': False})
            except:
                return render(request, "Student/reportRequest.html", {'success': False})
        return redirect('index')