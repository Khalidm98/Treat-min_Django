from django.contrib import admin
from .models import *


class CityAdmin(admin.ModelAdmin):
    list_display = ['name', 'id']


class AreaAdmin(admin.ModelAdmin):
    list_display = ['name', 'id']


admin.site.register(City, CityAdmin)
admin.site.register(Area, AreaAdmin)
