from django.http.request import HttpHeaders
from django.shortcuts import render
from django.shortcuts import HttpResponse
from . import forms
from . import models
from UserAuthentication.models import User

# Create your views here.

def add_course(request):
    user: User = User.objects.get(pk=request.user.id)

    if user.is_admin():
        form = forms.add_course_form(request.POST or None)

        if form.is_valid():
            course = models.Course(university=form.cleaned_data['university'], 
                                course_name=form.cleaned_data['course_name'],
                                description=form.cleaned_data['description'])
            if models.Course.objects.filter(university=course.university).exists() and models.Course.objects.filter(course_name=course.course_name).exists():
                return HttpResponse("El curso \"" + course.course_name + "\" ya estaba registrado")
            course.save()
        context = {
            'form': form
        }
        return render(request, "adminCrudForm.html", context)

    else:
        return render(request, 'UserAuthentication/index.html')    
