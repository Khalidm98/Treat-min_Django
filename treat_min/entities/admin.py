from django.contrib import admin
from .models import Clinic, Room, Service, Doctor, Hospital
from ..entities_details.admin import ClinicDetailInline, RoomDetailInline, ServiceDetailInline


class ClinicAdmin(admin.ModelAdmin):
    inlines = [ClinicDetailInline]
    list_display = ['name']
    search_fields = ['name']


class RoomAdmin(admin.ModelAdmin):
    inlines = [RoomDetailInline]
    list_display = ['name']
    search_fields = ['name']


class ServiceAdmin(admin.ModelAdmin):
    inlines = [ServiceDetailInline]
    list_display = ['name']
    search_fields = ['name']


class DoctorAdmin(admin.ModelAdmin):
    inlines = [ClinicDetailInline]
    list_display = ['name', 'speciality']
    search_fields = ['name', 'title', 'phone']


class HospitalAdmin(admin.ModelAdmin):
    inlines = [ClinicDetailInline, RoomDetailInline, ServiceDetailInline]
    list_display = ['name']
    search_fields = ['name', 'phone']

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
admin.site.register(Room, RoomAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Hospital, HospitalAdmin)
