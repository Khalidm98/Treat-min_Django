from datetime import date
from django.contrib import admin, messages
from django.utils.translation import ngettext, gettext_lazy as _
from .models import ClinicAppointment, ServiceAppointment


class AppointmentAdmin(admin.ModelAdmin):
    readonly_fields = ['booking_date']
    actions = ['accept', 'reject']
    list_display = ['appointment_date', 'schedule', 'user', 'status', 'booking_date']

    @admin.action(description=_('Accept selected Appointments'))
    def accept(self, request, queryset):
        updated = queryset.update(status='A')
        self.message_user(request, ngettext(
            _('%d appointment was successfully accepted.'),
            _('%d appointments were successfully accepted.'),
            updated,
        ) % updated, messages.SUCCESS)

    @admin.action(description=_('Reject selected Appointments'))
    def reject(self, request, queryset):
        updated = queryset.update(status='R')
        self.message_user(request, ngettext(
            _('%d appointment was successfully rejected.'),
            _('%d appointments were successfully rejected.'),
            updated,
        ) % updated, messages.SUCCESS)

    def get_readonly_fields(self, request, obj=None):
        if hasattr(request.user, 'hospital_admin'):
            if obj.appointment_date < date.today() or obj.status == 'C':
                return ['status', 'schedule', 'appointment_date', 'user', 'booking_date']
            return ['schedule', 'appointment_date', 'user', 'booking_date']
        else:
            return super().get_readonly_fields(request, obj=None)

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if hasattr(request.user, 'hospital_admin'):
            if db_field.name == 'status':
                kwargs['choices'] = [
                    ('A', 'Accepted'),
                    ('R', 'Rejected'),
                ]
        return super().formfield_for_choice_field(db_field, request, **kwargs)


class ClinicAppointmentAdmin(AppointmentAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if hasattr(request.user, 'hospital_admin'):
            return qs.filter(schedule__clinic__hospital=request.user.hospital_admin.hospital)
        return qs


class ServiceAppointmentAdmin(AppointmentAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if hasattr(request.user, 'hospital_admin'):
            return qs.filter(schedule__service__hospital=request.user.hospital_admin.hospital)
        return qs


admin.site.register(ClinicAppointment, ClinicAppointmentAdmin)
admin.site.register(ServiceAppointment, ServiceAppointmentAdmin)
