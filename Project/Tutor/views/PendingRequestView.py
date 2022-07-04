from django.views.generic.list import ListView
from UserAuthentication.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from Tutor.models import Tutor, TutorAvailableSchedule
from Student.models import Request
from Tutorship.models import Tutorship, RequestNotification


def deny_request(request_id):
    request_to_deny = Request.objects.get(pk=request_id)
    request_to_deny.state = 'DN'
    request_to_deny.save()

    notification = RequestNotification(
        notification_type='RR',
        to_user=request_to_deny.user_requester,
        from_user=request_to_deny.tutor_requested,
        request=request_to_deny
    )
    notification.save()


class PendingRequestView(ListView):
    template_name = 'Tutor/tutorRequest.html'
    context_object_name = 'requests'

    def __init__(self, *args, **kwargs):
        self.user = None
        super(PendingRequestView, self).__init__(*args, **kwargs)

    def get_queryset(self, *args):
        return Request.objects.filter(tutor_requested_id=self.user.id, state='PN').order_by('date_start')

    def get_context_data(self, **kwargs):
        context = super(PendingRequestView, self).get_context_data(**kwargs)
        context['title_page'] = "Solicitudes Pendientes"
        context['select_navbar_tutorships'] = 1
        return context

    def handle_get(self, request, request_pk):
        if not self.user.is_tutor():
            return

        if request.GET.get('accion') == 'ver':
            pass
        elif request.GET.get('accion') == 'rechazar':
            deny_request(request_pk)
            messages.add_message(request, messages.SUCCESS, 'La tutoría ha sido rechazada')
        elif request.GET.get('accion') == 'aceptar':
            user = self.user
            request_tutorship = Request.objects.get(pk=request_pk, tutor_requested_id=user)
            request_tutorship.state = 'AP'
            request_tutorship.save()
            messages.add_message(request, messages.SUCCESS, 'La tutoría ha sido aceptada')

            tutorship = Tutorship(
                max_people=50,
                request=request_tutorship
            )
            tutorship.save()

            start_date = request_tutorship.date_start
            tutorship_start_date = start_date.strftime("%Y-%m-%d %H:%M")

            end_date = request_tutorship.date_end
            tutorship_end_date = end_date.strftime("%Y-%m-%d %H:%M")

            # reject the other requests
            query_set = list(Request.objects.filter(tutor_requested_id=user,
                                                    state='PN',
                                                    date_start__gte=tutorship_start_date))
            for tutorship_to_check in query_set:
                date_start = tutorship_to_check.date_start
                clean_date_start = date_start.strftime("%Y-%m-%d %H:%M")
                date_end = tutorship_to_check.date_end
                clean_date_end = date_end.strftime("%Y-%m-%d %H:%M")

                if tutorship_start_date < clean_date_end and clean_date_start < tutorship_end_date:
                    tutorship_to_check.state = 'DD'
                    tutorship_to_check.save()

                    notification = RequestNotification(
                        notification_type='RR',
                        to_user=tutorship_to_check.user_requester,
                        from_user=tutorship_to_check.tutor_requested,
                        request=tutorship_to_check
                    )
                    notification.save()

            schedule_selected = list(TutorAvailableSchedule.objects.filter(user=user,
                                                                           start_time__lte=tutorship_start_date,
                                                                           end_time__gte=tutorship_end_date))

            for schedule in schedule_selected:
                date_start = schedule.start_time
                schedule_date_start = date_start.strftime("%Y-%m-%d %H:%M")
                date_end = schedule.end_time
                schedule_date_end = date_end.strftime("%Y-%m-%d %H:%M")

                if schedule_date_start == tutorship_start_date and schedule_date_end == tutorship_end_date:
                    schedule.delete()
                elif schedule_date_start == tutorship_start_date:
                    schedule.start_time = tutorship_end_date
                    schedule.save()
                    print("HORA INICIO AL INICIO DEL HORARIO")
                elif schedule_date_end == tutorship_end_date:
                    schedule.end_time = tutorship_start_date
                    schedule.save()
                    print("HORA FINAL AL FINAL DEL HORARIO")
                else:
                    new_end_time = schedule_date_end
                    schedule.end_time = tutorship_start_date
                    scheduled_block = TutorAvailableSchedule(
                        user_id=user.id,
                        start_time=tutorship_end_date,
                        end_time=new_end_time,
                    )
                    schedule.save()
                    scheduled_block.save()
                    print("AGENDÓ EN EL CENTRO DEL HORARIO")

            notification = RequestNotification(
                notification_type='AR',
                to_user=request_tutorship.user_requester,
                from_user=request_tutorship.tutor_requested,
                request=request_tutorship
            )
            notification.save()

    def get(self, request, request_pk=None, *args, **kwargs):
        self.user = User.objects.get(pk=request.user.id)
        self.handle_get(request, request_pk)
        return super(PendingRequestView, self).get(request, *args, **kwargs)
