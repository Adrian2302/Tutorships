from django.views import generic
from django.shortcuts import redirect, render
from django.contrib import messages

from UserAuthentication.models import User
from Tutorship.models import Tutorship, TutorshipScore
from Student.models import Requesters
from Student.models import Request
from Tutor.models import Tutor


def create_context(query_set, query_set2):
    return {'tutorships': query_set, 'join_tutorships' : query_set2, 'title_page' : "Historial", 'my_tutorships' : 1}


class doneTutorships(generic.View):

    def get(self, request):
        user = User.objects.get(pk=request.user.id)
        if user.is_student():
            requesters = Requesters.objects.filter(user_requester=user).values_list('request', flat=True)

            query_set = list(Tutorship.objects.filter(state='DN')
                             .select_related('request')
                             .filter(request__user_requester=user))

            query_set2 = list(Tutorship.objects.filter(state='DN')
                             .select_related('request')
                             .filter(request__id__in=requesters))

            
            context = create_context(query_set, query_set2)
            return render(request, "Student/studentHistory.html", context)
        else:
            return redirect('index')

    def post(self, request):
        id_request = request.POST.get('tutorship')
        score = request.POST.get('score_options')
        comment_student = request.POST.get('comment_student')
        tutorship = Tutorship.objects.get(pk=id_request)

        tutorship_score = TutorshipScore(
            tutorship=tutorship,
            score=score,
            student_comment=comment_student,
        )
        tutorship_score.save()
        messages.add_message(request, messages.SUCCESS, 'Puntuación enviada exitosamente')
        
        return redirect('student_done_request')
