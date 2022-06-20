from django.contrib import admin
from Region.models import Regions


class RegionAdmin(admin.ModelAdmin):
    pass


admin.site.register(Regions, RegionAdmin)
