from django.views import generic
from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from django.conf import settings

from Course.models import Course
from Session.models import Session
from Modality.models import Modality
from Payment.models import Payment
from UserAuthentication.models import User
from Tutor.models import TutorCourse
from Student.filtersModels import ListTypeSearch

def create_context(search_query, page_number, type_search, filters):
    try:

        results, type_list = handlers_results(search_query, type_search, filters)

        page_display = get_paginator_results(results, page_number)

        sessions = Session.objects.all()
        modals = Modality.objects.all()
        retributions = Payment.objects.all()

        if type_search == None:
            type_search = "cursos"
        
        context = {
                'latest_search': search_query,
                'results': page_display,
                'types_searches': type_list,
                'sessions': sessions,   
                'modals': modals,
                'retributions' : retributions, 
                'last_type': type_search
            }
    except Exception as e:
        print(e)
        raise Exception ("Error en la busqueda")

    return context


def get_paginator_results(results, page_number):
    if results is not None:

        if page_number is None:
            page_number = 1

        paginator = Paginator(results, settings.PAGE_SIZE)
        page_display = paginator.get_page(page_number)
        return page_display
    return results


def get_results_course(search_query):
    if search_query == "all" or search_query == "":
        results = Course.objects.all().order_by('course_name')
    else:
        results = Course.objects.filter(course_name__icontains=search_query).order_by('course_name')


    return results


def get_results_university(search_query):
    if search_query == "all" or search_query == "":
        results = Course.objects.all().order_by('course_name')
    else:
        results = Course.objects.filter(university=search_query).order_by('course_name')

    return results


def get_results_tutor(search_query, filters):
    if search_query == "all" or search_query == "":
        results = User.objects.filter(type=2).order_by('name', 'lastname')
    else:
        fullname = search_query.split(' ')
        if len(fullname) == 2:
            results = User.objects.filter(name__icontains=fullname[0], lastname__icontains=fullname[1], type=2).order_by('name', 'lastname')
        else:
            results = User.objects.filter(name__icontains=fullname[0], type=2).order_by('name', 'lastname')

    results = do_filters(filters)
    return results
    

def handlers_results(search_query, type_search, filters):

    if type_search == "universidad":
        type_list = get_list_type_search(1)
        results = get_results_university(search_query)
    elif type_search == "tutor":
        type_list = get_list_type_search(2)
        results = get_results_tutor(search_query, filters)
    elif type_search == "recursos-publicos":
        pass
    elif type_search == "sesiones-abiertas":
        pass
    else:
        type_list = get_list_type_search(0)
        results = get_results_course(search_query)
        
    return results, type_list


def get_list_type_search(selected_type_search):
    list_type_search = ListTypeSearch([0,0,0,0,0], ['cursos', 'universidad', 'tutor', 'recursos-publicos', 'sesiones-abiertas'])
    list_type_search.list[selected_type_search].selected = 1
    return list_type_search.list


def do_filters(filters):
    pass


def filter_session(last_query, session_names):
    pass


def filter_modality(last_query, modality_names):
    pass


def get_filters(request):
    filters = {}

    if request.GET.get('sesion'):
        filters['session'] = request.GET.get('sesion')
    
    if request.GET.getlist('modalidad'):
        filters['modality'] = request.GET.get('modalidad')

    if request.GET.get('retribución'):
        filters['payment'] = request.GET.get('retribución')

    if request.GET.get('calificacion'):
        filters['score'] = request.GET.get('calificacion')

    if request.GET.get('region'):
        pass

    return filters


class searchCourse(generic.View):

    def get(self, request, type_search):
        try:
            search_query = request.GET.get('buscar')
            page_number = request.GET.get('pagina') 

            if search_query is None:
                return redirect('index')

            filters = get_filters(request)

            context = create_context(search_query, page_number, type_search, filters)      
        except:
            context = {}

        if type_search == "tutor":
            return render(request, 'Student/searchTutor.html', context)
        else:
            return render(request, "Student/search.html", context)
