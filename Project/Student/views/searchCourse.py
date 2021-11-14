from django.views import generic
from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from django.core.cache import cache
from django.conf import settings

from Course.models import Course
from Session.models import Session
from Modality.models import Modality
from UserAuthentication.models import TutorCourse, User

def create_context(search_query, page_number):	

    results = get_results(search_query)

    page_display = get_paginator_results(results, page_number)

    sessions = Session.objects.all()
    modals = Modality.objects.all()

    context = {
            'latest_search': search_query,
            'results': page_display,
            'sessions': sessions,
            'modals': modals
        }

    return context

def get_paginator_results(results, page_number):
    if results is not None:
        if page_number is None:
            page_number = 1

        paginator = Paginator(results, settings.PAGE_SIZE)
        page_display = paginator.get_page(page_number)
        return page_display
    return results

def get_results(search_query):
    results = None
    if cache.get('latest_search') == search_query and cache.get('latest_results') is not None:
        results = cache.get('latest_results')
    else:
        if search_query == "all" or search_query == "":
            results = Course.objects.all().order_by('course_name')
        else:
            results = Course.objects.filter(course_name__icontains=search_query).order_by('course_name')
        cache.set('latest_search', search_query)
    cache.set('latest_results', results)

    return results

def get_results_by_filters(search_query, filters):
    results = None

def filter_tutor(last_query, tutor_fullname):
    split_name = tutor_fullname.split(' ')
    tutor = User.objects.filter(name=split_name[0], lastname=split_name[1])

    if tutor is not None and tutor.is_tutor():
        query_tutor_course = TutorCourse.objects.filter(user=tutor)
        query_result = Course.objects.filter(tutor=tutor)
    pass

def filter_session(last_query, session_names):
    pass

def filter_modality(last_query, modality_names):
    pass

def get_filters(request):
    filters = {}

    if request.GET.get('filtroTutor'):
        filters.update({'tutor': request.GET.get('filtroTutor')})

    if request.GET.getlist('filtroModalidad'):
        filters.update({'modality': request.GET.getlist('filtroModalidad')})
    
    if request.GET.getlist('filtroSesion'):
        filters.update({'session': request.GET.getlist('filtroSesion')})
        
    return filters

class searchCourse(generic.View):

    def get(self, request):
        search_query = request.GET.get('buscar')
        page_number = request.GET.get('pagina') 

        if search_query is None:
            return redirect('index')

        context = create_context(search_query, page_number)
        
        return render(request, "Student/search.html", context)