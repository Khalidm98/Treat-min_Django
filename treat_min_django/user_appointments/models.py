from django.db import models
from django.utils.translation import gettext_lazy as _
from ..accounts.models import User
from ..entities_details.models import ClinicSchedule, RoomSchedule, ServiceSchedule

STATUS = [
    ('A', _('Accepted')),
    ('C', _('Canceled')),
    ('R', _('Rejected')),
    ('W', _('Waiting'))
]


class Appointment(models.Model):
    status = models.CharField(max_length=1, choices=STATUS, default='W',verbose_name=_('status'))
    booking_date = models.DateTimeField(auto_now_add=True,verbose_name=_('booking_date'))
    appointment_date = models.DateField(verbose_name=_('appointment_date'))

    class Meta:
        abstract = True



class ClinicAppointment(Appointment):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='clinics_appointments',verbose_name=_('user'))
    schedule = models.ForeignKey(ClinicSchedule, null=True, on_delete=models.SET_NULL, related_name='appointments',verbose_name=_('schedule'))

    class Meta:
        verbose_name_plural = _('Clinics Appointments')
        verbose_name = _('clinic appointment')
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'schedule', 'appointment_date'], name='unique_clinic_appointment'
            )
        ]

    def __str__(self):
        return self.user.user.email + " - " + str(self.booking_date)[0:19]


class RoomAppointment(Appointment):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rooms_appointments',verbose_name=_('user'))
    schedule = models.ForeignKey(RoomSchedule, null=True, on_delete=models.SET_NULL, related_name='appointments',verbose_name=_('schedule'))

    class Meta:
        verbose_name_plural = _('Rooms Appointments')
        verbose_name = _('room appointment')
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'schedule', 'appointment_date'], name='unique_room_appointment'
            )
        ]

    def __str__(self):
        return self.user.user.email + " - " + str(self.booking_date)[0:19]


class ServiceAppointment(Appointment):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='services_appointments',verbose_name=_('user'))
    schedule = models.ForeignKey(ServiceSchedule, null=True, on_delete=models.SET_NULL, related_name='appointments',verbose_name=_('schedule'))

    class Meta:
        verbose_name_plural = _('Services Appointments')
        verbose_name = _('service appointment')
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'schedule', 'appointment_date'], name='unique_service_appointment'
            )
        ]

    def __str__(self):
        return self.user.user.email + " - " + str(self.booking_date)[0:19]
