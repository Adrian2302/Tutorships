from django.views import generic
from django.views.generic.edit import CreateView
from django import forms
from Tutor.forms import ProfileForm
from Tutor.forms import ProfilePaymentForm
from Tutor.forms import ProfileSessionForm
from Tutor.forms import ProfileModalityForm
from UserAuthentication.models import User
from django.shortcuts import render, redirect
from Tutor.models import Tutor
from Session.models import Session
from Modality.models import Modality
from Payment.models import Payment


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
        form = ProfileForm(request.GET or None, **{'user': user})
        payment_form = ProfilePaymentForm(request.GET or None, **{'user': user})
        session_form = ProfileSessionForm(request.GET or None, **{'user': user})
        modality_form = ProfileModalityForm(request.GET or None, **{'user': user})

        if user.is_tutor():
            return render(request, self.template_name, create_context(form,
                                                                      payment_form,
                                                                      session_form,
                                                                      modality_form
                                                                      ))
        else:
            redirect('index')

    def post(self, request):
        form = ProfileForm(request.POST or None)
        payment_form = ProfilePaymentForm(request.POST or None)
        session_form = ProfileSessionForm(request.POST or None)
        modality_form = ProfileModalityForm(request.POST or None)

        if form.is_valid() and payment_form.is_valid() and session_form.is_valid() and modality_form.is_valid():
            tutor = Tutor.objects.get(user_id=request.user.id)
            tutor.amount_per_person = form.cleaned_data['tutorship_price']
            tutor.increment_per_half_hour = form.cleaned_data['increment_half_hour']
            tutor.payment_type = Payment.objects.get(
                name=payment_form.cleaned_data['choices_payment'])
            tutor.session_type = Session.objects.get(
                name=session_form.cleaned_data['choices_session'])
            tutor.modality_type = Modality.objects.get(
                name=modality_form.cleaned_data['choices_modality'])
            tutor.save()

        return render(request, self.template_name, create_context(form,
                                                                  payment_form,
                                                                  session_form,
                                                                  modality_form))
