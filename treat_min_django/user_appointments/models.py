from django.db import models
from treat_min_django.accounts.models import User
from treat_min_django.entities_details.models import ClinicSchedule, RoomSchedule, ServiceSchedule

STATUS = [
    ('A', 'Accepted'),
    ('C', 'Canceled'),
    ('R', 'Rejected'),
    ('W', 'Waiting')
]


class Appointment(models.Model):
    status = models.CharField(max_length=1, choices=STATUS, default='W')
    booking_date = models.DateTimeField(auto_now_add=True)
    appointment_date = models.DateField()

    class Meta:
        abstract = True


class ClinicAppointment(Appointment):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='clinics_appointments')
    schedule = models.ForeignKey(ClinicSchedule, null=True, on_delete=models.SET_NULL, related_name='appointments')

    class Meta:
        verbose_name_plural = 'Clinics Appointments'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'schedule', 'appointment_date'], name='unique_clinic_appointment'
            )
        ]

    def __str__(self):
        return self.user.user.email + " - " + str(self.booking_date)[0:19]


class RoomAppointment(Appointment):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rooms_appointments')
    schedule = models.ForeignKey(RoomSchedule, null=True, on_delete=models.SET_NULL, related_name='appointments')

    class Meta:
        verbose_name_plural = 'Rooms Appointments'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'schedule', 'appointment_date'], name='unique_room_appointment'
            )
        ]

    def __str__(self):
        return self.user.user.email + " - " + str(self.booking_date)[0:19]


class ServiceAppointment(Appointment):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='services_appointments')
    schedule = models.ForeignKey(ServiceSchedule, null=True, on_delete=models.SET_NULL, related_name='appointments')

    class Meta:
        verbose_name_plural = 'Services Appointments'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'schedule', 'appointment_date'], name='unique_service_appointment'
            )
        ]

    def __str__(self):
        return self.user.user.email + " - " + str(self.booking_date)[0:19]
