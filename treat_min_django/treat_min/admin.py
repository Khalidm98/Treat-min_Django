from django.contrib import admin
from .models import *

SCHEDULE_FIELDS = [
    'price', 'sat_from', 'sat_to', 'sun_from', 'sun_to', 'mon_from', 'mon_to',
    'tue_from', 'tue_to', 'wed_from', 'wed_to', 'thu_from', 'thu_to', 'fri_from', 'fri_to'
]

APPOINTMENT_FIELDS = ['schedule', 'user', 'appointment_date', 'status', 'booking_date']


class ClinicScheduleInline(admin.TabularInline):
    model = ClinicSchedule
    fields = ['hospital', 'clinic', 'doctor'] + SCHEDULE_FIELDS
    extra = 1


class RoomScheduleInline(admin.TabularInline):
    model = RoomSchedule
    fields = ['hospital', 'room'] + SCHEDULE_FIELDS
    extra = 1


class ServiceScheduleInline(admin.TabularInline):
    model = ServiceSchedule
    fields = ['hospital', 'service'] + SCHEDULE_FIELDS
    extra = 1


class ClinicAdmin(admin.ModelAdmin):
    inlines = [ClinicScheduleInline]


class RoomAdmin(admin.ModelAdmin):
    inlines = [RoomScheduleInline]


class ServiceAdmin(admin.ModelAdmin):
    inlines = [ServiceScheduleInline]


class DoctorAdmin(admin.ModelAdmin):
    inlines = [ClinicScheduleInline]


class HospitalAdmin(admin.ModelAdmin):
    inlines = [ClinicScheduleInline, RoomScheduleInline, ServiceScheduleInline]


class ClinicScheduleAdmin(admin.ModelAdmin):
    fields = ['hospital', 'clinic', 'doctor'] + SCHEDULE_FIELDS


class RoomScheduleAdmin(admin.ModelAdmin):
    fields = ['hospital', 'room'] + SCHEDULE_FIELDS


class ServiceScheduleAdmin(admin.ModelAdmin):
    fields = ['hospital', 'service'] + SCHEDULE_FIELDS


class AppointmentAdmin(admin.ModelAdmin):
    fields = APPOINTMENT_FIELDS


admin.site.register(Clinic, ClinicAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Service, ServiceAdmin)

admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Hospital, HospitalAdmin)

admin.site.register(ClinicSchedule, ClinicScheduleAdmin)
admin.site.register(RoomSchedule, RoomScheduleAdmin)
admin.site.register(ServiceSchedule, ServiceScheduleAdmin)

admin.site.register(ClinicAppointment, AppointmentAdmin)
admin.site.register(RoomAppointment, AppointmentAdmin)
admin.site.register(ServiceAppointment, AppointmentAdmin)
