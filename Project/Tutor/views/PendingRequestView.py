from django.views import generic
from django.views.generic.edit import CreateView
from django.views.generic import ListView
from django import forms
from UserAuthentication.models import User
from django.shortcuts import render, redirect
from Tutor.models import Tutor
from Session.models import Session
from Modality.models import Modality
from Payment.models import Payment
from Student.models import Request
from Student.models import Requesters
from Tutorship.models import Tutorship


def create_context(user):
    query_set = list(Request.objects.filter(tutor_requested_id=user, state='PN').order_by('date_start'))
    context = {'requests': query_set}
    return context


class PendingRequestView(generic.View):
    template_name = 'Tutor/tutorRequest.html'
    user: User = None

    def get(self, request, request_pk=None):
        user = User.objects.get(pk=request.user.id)
        if user.is_tutor():
            if request.GET.get('accion') == 'rechazar':
                request = Request.objects.get(pk=request_pk, tutor_requested_id=user)
                request.state = 'DD'
                request.save()
                return redirect('tutor_pending_requests')
            elif request.GET.get('accion') == 'aceptar':
                request = Request.objects.get(pk=request_pk, tutor_requested_id=user)
                request.state = 'AP'
                request.save()

                tutorship = Tutorship(
                    max_people=1,
                    name='Tutoría',
                    description='Descripción de tutoría',
                    request=request
                )

                tutorship.save()

                return redirect('tutor_pending_requests')
            return render(request, self.template_name, context=create_context(user))
        else:
            return redirect('index')
