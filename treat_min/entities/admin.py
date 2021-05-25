from django.contrib import admin
from .models import Clinic, Service, Doctor, Hospital
from ..entities_details.admin import ClinicDetailInline, ServiceDetailInline


class ClinicAdmin(admin.ModelAdmin):
    inlines = [ClinicDetailInline]
    list_display = ['name', 'id']
    search_fields = ['name']


class ServiceAdmin(admin.ModelAdmin):
    inlines = [ServiceDetailInline]
    list_display = ['name', 'id']
    search_fields = ['name']


class DoctorAdmin(admin.ModelAdmin):
    inlines = [ClinicDetailInline]
    list_display = ['name', 'speciality', 'id']
    search_fields = ['name', 'title', 'phone']

    def get_exclude(self, request, obj=None):
        if hasattr(request.user, 'hospital_admin') and not (obj is None):
            return ['phone']
        return []


class HospitalAdmin(admin.ModelAdmin):
    inlines = [ClinicDetailInline, ServiceDetailInline]
    list_display = ['name', 'city', 'area', 'id']
    search_fields = ['name', 'phone', 'city__name', 'area__name']
    autocomplete_fields = ['city', 'area']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if hasattr(request.user, 'hospital_admin'):
            return qs.filter(id=request.user.hospital_admin.hospital.id)
        return qs

    def get_readonly_fields(self, request, obj=None):
        if hasattr(request.user, 'hospital_admin'):
            return ['name', 'address', 'latitude', 'longitude', 'photo']
        else:
            return super().get_readonly_fields(request, obj)


admin.site.register(Clinic, ClinicAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Hospital, HospitalAdmin)
