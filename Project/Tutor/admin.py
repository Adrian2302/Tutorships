from django.contrib import admin
from .models import TutorAvailableSchedule


class TutorAvailableScheduleAdmin(admin.ModelAdmin):
    pass


admin.site.register(TutorAvailableSchedule, TutorAvailableScheduleAdmin)

