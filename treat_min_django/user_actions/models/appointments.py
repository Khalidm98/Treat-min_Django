from django.db import models
from ...accounts.models import User
from ...entities.models import ClinicSchedule, RoomSchedule, ServiceSchedule

STATUS = [
    ('A', 'Accepted'),
    ('C', 'Canceled'),
    ('R', 'Rejected'),
    ('W', 'Waiting')
]


class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=STATUS, default='W')
    booking_date = models.DateTimeField(auto_now_add=True)
    appointment_date = models.DateField()

    class Meta:
        abstract = True

    def __str__(self):
        return self.user.user.email + " - " + str(self.booking_date)[0:19]


class ClinicAppointment(Appointment):
    schedule = models.ForeignKey(ClinicSchedule, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name_plural = 'Clinics Appointments'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'schedule', 'appointment_date'], name='unique_clinic_appointment'
            )
        ]


class RoomAppointment(Appointment):
    schedule = models.ForeignKey(RoomSchedule, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name_plural = 'Rooms Appointments'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'schedule', 'appointment_date'], name='unique_room_appointment'
            )
        ]


class ServiceAppointment(Appointment):
    schedule = models.ForeignKey(ServiceSchedule, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name_plural = 'Services Appointments'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'schedule', 'appointment_date'], name='unique_service_appointment'
            )
        ]
