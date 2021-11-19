from django.views.generic import View
from django.shortcuts import render

from UserAuthentication.models import User
from Student.models import Request
from Tutorship.models import Tutorship
from Resource.models import ResourceTutorship
from Tutor.forms import EditTutorshipInfo


class TutorshipView(View):
    template_name = 'Tutor/tutorshipView.html'
    user: User = None

    def get(self, request, request_pk=None):
        user = User.objects.get(pk=request.user.id)
        if user.is_tutor():
            tutorship_request = Request.objects.get(pk=request_pk, tutor_requested_id=user)
            tutorship = Tutorship.objects.get(request=tutorship_request)
            resources = [resource for query_set.resource in list(ResourceTutorship.objects.filter(tutorship=tutorship))]
            form_info = EditTutorshipInfo(instance=tutorship)
            context = {
                'form_info': form_info,
                'tutorship_request': tutorship_request,
                'tutorship': tutorship,
                'resources': resources
            }
            return render(request, self.template_name, context)
        else:
            return redirect('index')
