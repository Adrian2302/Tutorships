from django.views import generic
from django.shortcuts import redirect, render
from django.contrib import messages

from UserAuthentication.models import User
from Tutorship.models import Tutorship, TutorshipScore


def create_context(query_set):
    return {'tutorships': query_set}


class doneTutorships(generic.View):

    def get(self, request):
        user = User.objects.get(pk=request.user.id)
        if user.is_student():

            query_set = list(Tutorship.objects.filter(state='DN')
                             .select_related('request')
                             .filter(request__user_requester=user))
            context = create_context(query_set)
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
        messages.success(request, 'Puntuación enviada exitosamente')
        tutorship_score.save()
        return redirect('student_done_request')
