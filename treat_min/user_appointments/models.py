from django.db import models
from django.core.exceptions import ValidationError
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
    status = models.CharField(max_length=1, choices=STATUS, default='W', verbose_name=_('status'))
    booking_date = models.DateTimeField(auto_now_add=True, verbose_name=_('booking date'))
    appointment_date = models.DateField(verbose_name=_('appointment date'))

    class Meta:
        abstract = True

    def clean(self):
        if self.status == 'C':
            raise ValidationError("You cannot cancel an appointment!\nEither accept or reject it.")
        super().clean()


class ClinicAppointment(Appointment):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='clinics_appointments', verbose_name=_('user')
    )
    schedule = models.ForeignKey(
        ClinicSchedule, on_delete=models.CASCADE, related_name='appointments', verbose_name=_('schedule')
    )

    class Meta:
        verbose_name = _('clinic appointment')
        verbose_name_plural = _('Clinics Appointments')
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'schedule', 'appointment_date'], name='unique_clinic_appointment'
            )
        ]

    def __str__(self):
        return self.user.user.email + " - " + str(self.booking_date)[0:19]


class RoomAppointment(Appointment):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rooms_appointments', verbose_name=_('user'))
    schedule = models.ForeignKey(
        RoomSchedule, on_delete=models.CASCADE, related_name='appointments', verbose_name=_('schedule')
    )

    class Meta:
        verbose_name = _('room appointment')
        verbose_name_plural = _('Rooms Appointments')
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'schedule', 'appointment_date'], name='unique_room_appointment'
            )
        ]

    def __str__(self):
        return self.user.user.email + " - " + str(self.booking_date)[0:19]


class ServiceAppointment(Appointment):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='services_appointments', verbose_name=_('user')
    )
    schedule = models.ForeignKey(
        ServiceSchedule, on_delete=models.CASCADE, related_name='appointments', verbose_name=_('schedule')
    )

    class Meta:
        verbose_name = _('service appointment')
        verbose_name_plural = _('Services Appointments')
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'schedule', 'appointment_date'], name='unique_service_appointment'
            )
        ]

    def __str__(self):
        return self.user.user.email + " - " + str(self.booking_date)[0:19]
