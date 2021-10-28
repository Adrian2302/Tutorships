from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.core.cache import cache
from django.core.paginator import Paginator
from django.conf import settings
from Course.models import Course
# Create your views here.

def student_index(request):
    return render(request, 'Student/index.html')

    
def search_course(request): 
    search_query = request.GET.get("search_query")
    page_number = request.GET.get('page')

    if search_query=="all":
        results = Course.objects.all()
    else:
        if cache.get('latest_search') == search_query and cache.get('latest_results') is not None:
            results = cache.get('latest_results')
        else:
            results = Course.objects.filter(course_name__icontains=search_query)
            cache.set('latest_search', search_query)
        cache.set('latest_results', results)
    
    paginator = Paginator(results, settings.PAGE_SIZE)
    page_display = paginator.get_page(page_number)
    context={
        'latest_search': search_query,
        'results': page_display
    }
    return render(request, "Student/search.html", context)