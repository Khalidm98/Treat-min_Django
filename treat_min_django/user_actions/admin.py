from django.contrib import admin
from .models import *

APPOINTMENT_FIELDS = ['schedule', 'appointment_date', 'user', 'status', 'booking_date']
REVIEW_FIELDS = ['user', 'date', 'rating', 'review']


class AppointmentAdmin(admin.ModelAdmin):
    fields = APPOINTMENT_FIELDS
    readonly_fields = ['booking_date']


class ClinicAppointmentAdmin(AppointmentAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if hasattr(request.user, 'hospitaladmin'):
            return qs.filter(schedule__clinic__hospital=request.user.hospitaladmin.hospital)
        return qs


class RoomAppointmentAdmin(AppointmentAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if hasattr(request.user, 'hospitaladmin'):
            return qs.filter(schedule__room__hospital=request.user.hospitaladmin.hospital)
        return qs


class ServiceAppointmentAdmin(AppointmentAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if hasattr(request.user, 'hospitaladmin'):
            return qs.filter(schedule__service__hospital=request.user.hospitaladmin.hospital)
        return qs


class ClinicReviewAdmin(admin.ModelAdmin):
    fields = ['clinic'] + REVIEW_FIELDS
    readonly_fields = ['date']


class RoomReviewAdmin(admin.ModelAdmin):
    fields = ['room'] + REVIEW_FIELDS
    readonly_fields = ['date']


class ServiceReviewAdmin(admin.ModelAdmin):
    fields = ['service'] + REVIEW_FIELDS
    readonly_fields = ['date']


admin.site.register(ClinicAppointment, ClinicAppointmentAdmin)
admin.site.register(RoomAppointment, RoomAppointmentAdmin)
admin.site.register(ServiceAppointment, ServiceAppointmentAdmin)

admin.site.register(ClinicReview, ClinicReviewAdmin)
admin.site.register(RoomReview, RoomReviewAdmin)
admin.site.register(ServiceReview, ServiceReviewAdmin)
