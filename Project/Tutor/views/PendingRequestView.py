from django.views import generic
from django.views.generic.edit import CreateView
from django.views.generic import ListView
from django import forms
from UserAuthentication.models import User
from django.shortcuts import render, redirect
from Tutor.models import Tutor, TutorAvailableSchedule
from Session.models import Session
from Modality.models import Modality
from Payment.models import Payment
from Student.models import Request
from Student.models import Requesters
from Tutorship.models import Tutorship
from Tutorship.models import RequestNotification


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
                request_tutorship = Request.objects.get(pk=request_pk, tutor_requested_id=user)
                request_tutorship.state = 'DD'
                request_tutorship.save()

                # Create notification
                notification = RequestNotification(
                    notification_type='RR',
                    to_user=request_tutorship.user_requester,
                    from_user=request_tutorship.tutor_requested,
                    request=request_tutorship
                )
                notification.save()

                return redirect('tutor_pending_requests')
            elif request.GET.get('accion') == 'aceptar':
                request_tutorship = Request.objects.get(pk=request_pk, tutor_requested_id=user)
                request_tutorship.state = 'AP'
                request_tutorship.save()

                tutorship = Tutorship(
                    max_people=50,
                    request=request_tutorship
                )
                tutorship.save()

                start_date=request_tutorship.date_start
                tutorship_start_date=start_date.strftime("%Y-%m-%d %H:%M")

                end_date=request_tutorship.date_end
                tutorship_end_date=end_date.strftime("%Y-%m-%d %H:%M")

                # rejected other tutorships
                query_set = list(Request.objects.filter(tutor_requested_id=user,
                 state='PN',
                  date_start__gte=tutorship_start_date))
                for requests in query_set:
                    date_requests = requests.date_start
                    clean_date_requests = date_requests.strftime("%Y-%m-%d %H:%M")
                    if tutorship_start_date == clean_date_requests or tutorship_end_date > clean_date_requests:
                        requests.state = 'DD'
                        requests.save()

                        # Create notification
                        notification = RequestNotification(
                            notification_type='RR',
                            to_user=requests.user_requester,
                            from_user=requests.tutor_requested,
                            request=requests
                        )
                        notification.save()
                
                # change tutor calendar
                schedule_selected=list(TutorAvailableSchedule.objects.filter(user=user,
                 start_time__lte=tutorship_start_date,
                  end_time__gte=tutorship_end_date))

                for schedule in schedule_selected:
                    date_start=schedule.start_time
                    schedule_date_start=date_start.strftime("%Y-%m-%d %H:%M")
                    date_end=schedule.end_time
                    schedule_date_end=date_end.strftime("%Y-%m-%d %H:%M")

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
                            user_id=user,
                            start_time=tutorship_end_date,
                            end_time=new_end_time,
                        )
                        schedule.save()
                        scheduled_block.save()
                        print("AGENDÓ EN EL CENTRO DEL HORARIO")

                # Create notification
                notification = RequestNotification(
                    notification_type='AR',
                    to_user=request_tutorship.user_requester,
                    from_user=request_tutorship.tutor_requested,
                    request=request_tutorship
                )
                notification.save()

                return redirect('tutor_pending_requests')
            return render(request, self.template_name, context=create_context(user))
        else:
            return redirect('index')
