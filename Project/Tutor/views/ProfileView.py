from django.views import generic
from django.views.generic.edit import CreateView
from django import forms
from Tutor.forms import ProfileForm
from Tutor.forms import ProfilePaymentForm
from Tutor.forms import ProfileSessionForm
from Tutor.forms import ProfileModalityForm
from UserAuthentication.models import User
from django.shortcuts import render, redirect


def create_context(form,
                   payment_form,
                   session_form,
                   modality_form):
    context = {
        'form': form,
        'payment_form': payment_form,
        'session_form': session_form,
        'modality_form': modality_form
    }
    return context


class ProfileView(generic.View):
    template_name = 'Tutor/tutorProfile.html'
    user: User = None
    form_class: ProfileForm = ProfileForm

    def get(self, request):
        user: User = User.objects.get(pk=request.user.id)
        form = ProfileForm(request.GET or None)
        payment_form = ProfilePaymentForm(request.GET or None)
        session_form = ProfileSessionForm(request.GET or None)
        modality_form = ProfileModalityForm(request.GET or None)

        if user.is_tutor():
            return render(request, self.template_name, create_context(form,
                                                                      payment_form,
                                                                      session_form,
                                                                      modality_form
                                                                      ))
        else:
            redirect('index')

    def post(self, request):
        # form = self.form_class(request.POST)
        # user: User = User.objects.get(pk=request.user.id)
        # if form.is_valid():
        #     scheduled_block = models.TutorshipAvailableSchedule(
        #         user_id=user.id,
        #         start_time=form.cleaned_data['start_time'],
        #         end_time=form.cleaned_data['end_time'],
        #     )
        #     scheduled_block.save()
        # return render(request, self.template_name, create_context(user, form))
        pass
