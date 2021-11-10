from django.views import generic
from django.shortcuts import redirect, render

from UserAuthentication.models import User
from Student.models import Request

def create_context(query_set):
    return {'requests': query_set}

class rejectedRequests(generic.View):

    def get(self, request):
        user = User.objects.get(pk=request.user.id)
        if user.is_student():
            query_set = list(Request.objects.filter(user_requester=user, state='DD').order_by('date_start'))
            context = {'requests': query_set}
            return render(request, "Student/studentRequest.html", context)
        else:
            return redirect('index')