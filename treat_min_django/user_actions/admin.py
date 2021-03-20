from django.contrib import admin
from .models import *

APPOINTMENT_FIELDS = ['schedule', 'appointment_date', 'user', 'status', 'booking_date']
REVIEW_FIELDS = ['user', 'date', 'rating', 'review']


class AppointmentAdmin(admin.ModelAdmin):
    fields = APPOINTMENT_FIELDS
    readonly_fields = ['booking_date']


class ClinicReviewAdmin(admin.ModelAdmin):
    fields = ['clinic'] + REVIEW_FIELDS
    readonly_fields = ['date']


class RoomReviewAdmin(admin.ModelAdmin):
    fields = ['room'] + REVIEW_FIELDS
    readonly_fields = ['date']


class ServiceReviewAdmin(admin.ModelAdmin):
    fields = ['service'] + REVIEW_FIELDS
    readonly_fields = ['date']


admin.site.register(ClinicAppointment, AppointmentAdmin)
admin.site.register(RoomAppointment, AppointmentAdmin)
admin.site.register(ServiceAppointment, AppointmentAdmin)

admin.site.register(ClinicReview, ClinicReviewAdmin)
admin.site.register(RoomReview, RoomReviewAdmin)
admin.site.register(ServiceReview, ServiceReviewAdmin)
