from django.contrib import admin
from .models import *


class CityAdmin(admin.ModelAdmin):
    list_display = ['name', 'id']
    search_fields = ['name']


class AreaAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'id']
    search_fields = ['name', 'city__name']


admin.site.register(City, CityAdmin)
admin.site.register(Area, AreaAdmin)
