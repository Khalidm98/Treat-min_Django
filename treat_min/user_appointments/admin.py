from django.contrib import admin
from .models import *


class AppointmentAdmin(admin.ModelAdmin):
    readonly_fields = ['booking_date']
    list_display = ['appointment_date', 'schedule', 'user', 'status', 'booking_date']

    def get_readonly_fields(self, request, obj=None):
        if hasattr(request.user, 'hospital_admin'):
            return ['schedule', 'appointment_date', 'user', 'booking_date']
        else:
            return super().get_readonly_fields(request, obj=None)


class ClinicAppointmentAdmin(AppointmentAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if hasattr(request.user, 'hospital_admin'):
            return qs.filter(schedule__clinic__hospital=request.user.hospital_admin.hospital)
        return qs


class RoomAppointmentAdmin(AppointmentAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if hasattr(request.user, 'hospital_admin'):
            return qs.filter(schedule__room__hospital=request.user.hospital_admin.hospital)
        return qs


class ServiceAppointmentAdmin(AppointmentAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if hasattr(request.user, 'hospital_admin'):
            return qs.filter(schedule__service__hospital=request.user.hospital_admin.hospital)
        return qs


admin.site.register(ClinicAppointment, ClinicAppointmentAdmin)
admin.site.register(RoomAppointment, RoomAppointmentAdmin)
admin.site.register(ServiceAppointment, ServiceAppointmentAdmin)
