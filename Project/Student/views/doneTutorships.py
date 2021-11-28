from django.views import generic
from django.shortcuts import redirect, render
from django.contrib import messages

from UserAuthentication.models import User
from Tutorship.models import Tutorship, TutorshipScore
from Student.models import Requesters
from Student.models import Request
from Tutor.models import Tutor


def create_context(query_set, query_set2):
    return {'tutorships': query_set, 'join_tutorships' : query_set2}


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


        tutorship_request_id = Request.objects.get(pk=tutorship.request.id)

        query_set = list(Tutorship.objects.filter(state='DN')
                             .select_related('request')
                             .filter(request__tutor_requested=tutorship_request_id.tutor_requested))

        total_califications = 0
        sum_califications = 0

        for item in query_set:
            query_set2 = list(TutorshipScore.objects.filter(tutorship=item.id))

            for item2 in query_set2:
                sum_califications += 1
                total_califications += item2.score

        average_rating = total_califications / sum_califications

        tutor = Tutor.objects.get(user=tutorship_request_id.tutor_requested.id)
        tutor.average_rating = average_rating
        tutor.save()

        return redirect('student_done_request')
