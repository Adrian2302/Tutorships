from django.views.generic import View
from UserAuthentication.models import User
from Tutorship.models import RequestNotification
from Student.models import Request
from django.shortcuts import redirect, render


class RequestNotificationView(View):
    def get(self, request, notification_pk, request_pk, *args, **kwargs):
        notification = RequestNotification.objects.get(pk=notification_pk)
        request = Request.objects.get(pk=request_pk)

        notification.seen = True
        notification.save()

        return redirect('tutor_pending_requests', request_pk=request_pk)

