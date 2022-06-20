from django.contrib import admin
from UserAuthentication.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'name', 'lastname', 'type', 'photo_profile')
    list_display_links = ('id', 'email')
    search_fields = ('id', 'email', 'name', 'lastname')
    list_per_page = 25


admin.site.register(User, UserAdmin)
