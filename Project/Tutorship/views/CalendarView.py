from django.views import generic
from django import forms
from Tutorship.forms import TutorshipForm
from UserAuthentication.models import User
from django.shortcuts import render, redirect
from Tutorship import models


def create_context(user: User, form: TutorshipForm):
    events = models.TutorAvailableSchedule.objects.filter(
        user=user
    ).order_by('start_time')
    event_list = []
    for event in events:
        event_list.append(
            {
                'message': "Reservado: "
                           + event.start_time.strftime("%H:%M")
                           + " - " + event.end_time.strftime("%H:%M"),
                'start': event.start_time.strftime("%Y-%m-%d"),
                'end': event.end_time.strftime("%Y-%m-%d"),
            }
        )
    context = {
        'form': form,
        'events': event_list
    }
    return context


class CalendarView(generic.View):
    template_name = 'Tutorship/tutorCalendar.html'
    user: User = None
    form_class: TutorshipForm = TutorshipForm

    def get(self, request, *args, **kwargs):
        user = User.objects.get(pk=request.user.id)
        form = self.form_class()
        if user.is_tutor():
            return render(request, self.template_name, create_context(user, form))
        else:
            redirect('index')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        user: User = User.objects.get(pk=request.user.id)
        if form.is_valid():
            scheduled_block: TutorAvailableSchedule = models.TutorAvailableSchedule(
                user_id=user.id,
                start_time=form.cleaned_data['start_time'],
                end_time=form.cleaned_data['end_time'],
            )
            scheduled_block.save()
        return render(request, self.template_name, create_context(user, form))
