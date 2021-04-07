from .models import *
from ..entities_details.admin import *


class ClinicAdmin(admin.ModelAdmin):
    inlines = [ClinicDetailInline]
    list_display = ['name']


class RoomAdmin(admin.ModelAdmin):
    inlines = [RoomDetailInline]
    list_display = ['name']


class ServiceAdmin(admin.ModelAdmin):
    inlines = [ServiceDetailInline]
    list_display = ['name']


class DoctorAdmin(admin.ModelAdmin):
    inlines = [ClinicDetailInline]
    list_display = ['name', 'speciality']


class HospitalAdmin(admin.ModelAdmin):
    inlines = [ClinicDetailInline, RoomDetailInline, ServiceDetailInline]
    list_display = ['name']

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
