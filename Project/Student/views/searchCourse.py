from django.views import generic
from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from django.core.cache import cache
from django.conf import settings

from Course.models import Course
from Session.models import Session
from Modality.models import Modality

def create_context(search_query, page_number):	
    results = get_results(search_query)
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

    return context

def get_results(search_query):
    results = None
    if cache.get('latest_search') == search_query and cache.get('latest_results') is not None:
        results = cache.get('latest_results')
    else:
        if search_query == "all" or search_query == "":
            results = Course.objects.all()
        else:
            results = Course.objects.filter(course_name__icontains=search_query)
        cache.set('latest_search', search_query)
    cache.set('latest_results', results)

    return results

class searchCourse(generic.View):

    def get(self, request):
        search_query = request.GET.get('buscar')
        page_number = request.GET.get('pagina') 

        if search_query is None:
            return redirect('index')

        context = create_context(search_query, page_number)
        
        return render(request, "Student/search.html", context)