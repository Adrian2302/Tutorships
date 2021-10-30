from django.views.generic import TemplateView
from django import forms
from Tutor.forms import TutorScheduleForm
from Tutor import models
from UserAuthentication.models import User
from django.shortcuts import render, redirect


def create_context(user: User, form: TutorScheduleForm):
    events = models.TutorAvailableSchedule.objects.filter(
        user=user
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
    context = {
        'form': form,
        'events': event_list
    }
    return context


class CalendarView(TemplateView):
    template_name = 'Tutor/tutorCalendar.html'
    user: User = None
    form_class: TutorScheduleForm = TutorScheduleForm

    def get(self, request):
        user = User.objects.get(pk=request.user.id)
        form = self.form_class()
        if user.is_tutor():
            return render(request, self.template_name, create_context(user, form))
        else:
            redirect('index')

    def post(self, request):
        form = self.form_class(request.POST)
        user: User = User.objects.get(pk=request.user.id)
        if form.is_valid():
            scheduled_block = models.TutorAvailableSchedule(
                user_id=user.id,
                start_time=form.cleaned_data['start_time'],
                end_time=form.cleaned_data['end_time'],
            )
            scheduled_block.save()
        return render(request, self.template_name, create_context(user, form))
