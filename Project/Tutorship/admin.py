from django.contrib import admin
from .models import RequestNotification, Tutorship

# Register your models here.
class TutorshipAdmin(admin.ModelAdmin):
    pass


admin.site.register(RequestNotification)
admin.site.register(Tutorship, TutorshipAdmin)
