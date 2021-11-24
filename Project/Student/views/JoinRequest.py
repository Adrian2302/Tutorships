from django.views import generic
from django.shortcuts import redirect, render
from Student.models import Request

from UserAuthentication.models import User
from Student.models import Request, Requesters

def create_context(request, user):
    
    
    context = {
        'session' : request.session_requested.name,
        'modal' : request.modality_requested.name, 
        'tutor' : request.tutor_requested.name,
    }

    return context


def join_request(request, user):
    try:
        if check_max_guests(request):
            request.num_requesters += 1
            request.save()
            Requesters.objects.create(request=request, user_requester=user)
            return True
    except Exception as e:
        print(e)
    return False   


# Cambiar 50
def check_max_guests(request):
    if request.session_requested.name == "Grupal - Privada" or request.session_requested.name == "Grupal - Pública":
        if 50 > request.num_requesters:
            return True
    return False


class JoinRequest(generic.View):

    def get(self, request, request_id):
        user = User.objects.get(id=request.user.id)
        if request.user.is_authenticated and user.is_student():
            try:
                request_to_join = Request.objects.get(id=request_id)
                
                context = create_context(request_to_join, user)
                return render(request, 'Student/formJoinRequest.html', context)
            except:
                return render(request, "Student/reportRequest.html", {'success': False})
        return redirect('index')

    def post(self, request, request_id):
        user = User.objects.get(id=request.user.id)
        if request.user.is_authenticated and user.is_student():
            try:
                request_to_join = Request.objects.get(id=request_id)
                
                succeeded = join_request(request_to_join, user)

                return render(request, "Student/reportRequest.html", {'success': succeeded})
            except:
                return render(request, "Student/reportRequest.html", {'success': False})
        return redirect('index')