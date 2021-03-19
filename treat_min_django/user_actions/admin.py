from django.contrib import admin
from .models import *

APPOINTMENT_FIELDS = ['schedule', 'appointment_date', 'user', 'status', 'booking_date']


class AppointmentAdmin(admin.ModelAdmin):
    fields = APPOINTMENT_FIELDS
    readonly_fields = ['booking_date']


admin.site.register(ClinicAppointment, AppointmentAdmin)
admin.site.register(RoomAppointment, AppointmentAdmin)
admin.site.register(ServiceAppointment, AppointmentAdmin)
