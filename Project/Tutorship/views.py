from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from . import models
from . import forms
from UserAuthentication.models import User

# Create your views here.
from .models import Tutorship
from .models import TutorshipAvailableSchedule
from .models import CourseTutorship


def tutor_create_tutorship(request):
    user: User = User.objects.get(pk=request.user.id)

    if user.type == 2:
        form = forms.CreateTutorshipForm(request.POST or None)

        if form.is_valid():
            tutorship = models.Tutorship(maxPeople=form.cleaned_data['maxPeople'], 
                                        amountPerPerson=form.cleaned_data['amountPerPerson'],
                                        incrementPerHalfHour=form.cleaned_data['incrementPerHalfHour'],
                                        typeSession=form.cleaned_data['typeSession'],
                                        typeMode=form.cleaned_data['typeMode'])

            tutorship.save()

        form2 = forms.CreateTutorshipForm2(request.POST or None)

        if form2.is_valid():
            tutorshipAvailableSchedule = models.TutorshipAvailableSchedule(date=form.cleaned_data['date'], 
                                                                           startHour=form.cleaned_data['startHour'],
                                                                           endHour=form.cleaned_data['endHour'])

            tutorshipAvailableSchedule.save()

        context = {
            "CourseTutorship": CourseTutorship.objects.all(),
            "form": form,
            "form2": form2
        }
        
        return render(request, "Tutorship/createTutorship.html", context)

    else:
        return redirect('index')
