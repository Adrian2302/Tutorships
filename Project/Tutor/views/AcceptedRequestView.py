from django.views import generic
from django.shortcuts import render, redirect

from UserAuthentication.models import User
from Student.models import Request
from Tutorship.models import Tutorship
from Resource.models import ResourceTutorship


def create_context(user):
    query_set = list(Request.objects.filter(tutor_requested_id=user, state='AP').order_by('date_start'))
    amount_accepted = len(query_set)
    if amount_accepted == 1:
        message = 'Tienes 1 tutoría agendada.'
    elif amount_accepted > 1:
        message = 'Tienes ' + str(amount_accepted) + ' tutorías agendadas.'
    else:
        message = 'No tienes tutorías agendadas.'

    context = {
        'requests': query_set,
        'message': message}
    return context


class AcceptedRequestView(generic.View):
    template_name = 'Tutor/tutorRequestAccepted.html'
    user: User = None

    def get(self, request, request_pk=None):
        user = User.objects.get(pk=request.user.id)
        if user.is_tutor():
            if request.GET.get('accion') == 'terminada':
                request = Request.objects.get(pk=request_pk, tutor_requested_id=user)
                request.set_done()
                tutorship = Tutorship.objects.get(request=request)
                tutorship.set_done()
                return redirect('tutor_accepted_requests')
            elif request.GET.get('accion') == 'ver':
                return redirect('tutor_tutorship_view', request_pk=request_pk)
            return render(request, self.template_name, context=create_context(user))
        else:
            return redirect('index')
