from django.views import View
from django.http import JsonResponse
from UserAuthentication.models import User
from datetime import datetime, timedelta
from Tutor.models import TutorAvailableSchedule


class PostRecurringScheduleView(View):
    def post(self, request):
        if request.method == 'POST':
            user = User.objects.get(pk=request.user.id)

            start_day = datetime.strptime(request.POST['start_day'], '%Y-%m-%d')
            end_day = datetime.strptime(request.POST['end_day'], '%Y-%m-%d')

            start_time = datetime.strptime(request.POST['start_time'], '%H:%M')
            end_time = datetime.strptime(request.POST['end_time'], '%H:%M')         
        

            days = [start_day + timedelta(days=x) for x in range(0, (end_day - start_day).days + 1)]
            for day in days:
                scheduled_block = TutorAvailableSchedule(
                    user_id=user.id,
                    start_time=day + timedelta(hours=start_time.hour, minutes=start_time.minute),
                    end_time=day + timedelta(hours=end_time.hour, minutes=end_time.minute),
                )
                scheduled_block.save()

            return JsonResponse({'status': 'success'})