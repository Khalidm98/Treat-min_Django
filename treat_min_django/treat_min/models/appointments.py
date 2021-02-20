from treat_min_django.accounts.models import User
from django.db import models
from .schedules import ClinicSchedule, RoomSchedule, ServiceSchedule


STATUS = (
    ('Accepted', 'Accepted'),
    ('Canceled', 'Canceled'),
    ('Rejected', 'Rejected'),
    ('Waiting', 'Waiting'),
)


class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=8, choices=STATUS, default='Waiting')
    booking_date = models.DateTimeField(blank=True, null=True)
    appointment_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.user.email + " - " + str(self.booking_date)


class ClinicAppointment(Appointment):
    schedule = models.ForeignKey(ClinicSchedule, on_delete=models.CASCADE)


class RoomAppointment(Appointment):
    schedule = models.ForeignKey(RoomSchedule, on_delete=models.CASCADE)


class ServiceAppointment(Appointment):
    schedule = models.ForeignKey(ServiceSchedule, on_delete=models.CASCADE)
