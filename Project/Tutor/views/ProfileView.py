from django.views import generic
from django.views.generic.edit import CreateView
from django import forms

from Tutor.forms import ProfileForm
from UserAuthentication.models import User
from django.shortcuts import render, redirect
from Tutor.models import Tutor
from Session.models import Session
from Modality.models import Modality
from Payment.models import Payment


def create_context(modality_form):
    context = {
        'modality_form': modality_form
    }
    return context


class ProfileView(generic.View):
    template_name = 'Tutor/tutorProfile.html'
    user: User = None

    def get(self, request):
        user: User = User.objects.get(pk=request.user.id)
        profile_form = ProfileForm(request.GET or None, **{'user': user})

        if user.is_tutor():
            return render(request, self.template_name, {'form': profile_form})
        else:
            return redirect('index')

    def post(self, request):
        profile_form = ProfileForm(request.POST or None)

        if profile_form.is_valid():
            tutor = Tutor.objects.get(user_id=request.user.id)
            tutor.amount_per_person = profile_form.cleaned_data['tutorship_price']
            tutor.increment_per_half_hour = profile_form.cleaned_data['increment_half_hour']
            tutor.payment_type = Payment.objects.get(
                name=profile_form.cleaned_data['choices_payment'])
            tutor.session_type = Session.objects.get(
                name=profile_form.cleaned_data['choices_session'])
            tutor.modality_type = Modality.objects.get(
                name=profile_form.cleaned_data['choices_modality'])
            tutor.save()

        return render(request, self.template_name, {'form': profile_form})
