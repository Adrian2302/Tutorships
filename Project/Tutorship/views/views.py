from django.shortcuts import render, redirect
from Tutorship import models
from Tutorship import forms
from UserAuthentication.models import User
from Resource.models import Resource
from Resource.forms import ResourceForm
from Course.models import Course
from Modality.models import Modality
from Session.models import Session


def tutor_create_tutorship(request):
    user: User = User.objects.get(pk=request.user.id)

    if user.type == 2:
        form = forms.CreateTutorshipForm(request.POST or None)
        form2 = forms.CreateTutorshipForm2(request.POST or None)
        form3 = ResourceForm(request.POST or None)

        if form.is_valid() and form2.is_valid() and form3.is_valid():
            
            tutorship = models.Tutorship(max_people=form.cleaned_data['max_people'], 
                                        amount_per_person=form.cleaned_data['amount_per_person'],
                                        increment_per_half_hour=form.cleaned_data['increment_per_half_hour'],
                                        type_session=Session.objects.get(pk=request.POST.get('session_name')).id,
                                        type_mode=Modality.objects.get(pk=request.POST.get('modality_name')).id)
            
            tutorship.save()
            
            relationCourseTutorship = models.CourseTutorship(id_tutorship=tutorship, 
                                                             id_course=Course.objects.get(pk=request.POST.get('course_name')))
            relationCourseTutorship.save()
            
        #if form2.is_valid():
            tutorshipAvailableSchedule = models.TutorshipAvailableSchedule(date=form.data['date'], 
                                                                           start_hour=form.data['start_hour'],
                                                                           end_hour=form.data['end_hour'])

            tutorshipAvailableSchedule.save()

        #if form3.is_valid():
            resource = Resource(name=form.cleaned_data['name'],
                                is_public=form.cleaned_data['is_public'],
                                description=form.cleaned_data['description'],
                                url=form.cleaned_data['url'],
                                author=form.cleaned_data['author'])

            resource.save()

        context = {
            "CourseTutorship": Course.objects.all(),
            "TableSession": Session.objects.all(),
            "TableModality": Modality.objects.all(),
            "form": form,
            "form2": form2,
            "form3": form3
        }
        
        return render(request, "Tutorship/createTutorship.html", context)

    else:
        return redirect('index')
