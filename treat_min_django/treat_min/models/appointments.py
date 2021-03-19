from treat_min_django.accounts.models import User
from django.db import models
from .details import ClinicDetail, RoomDetail, ServiceDetail

STATUS = [
    ('A', 'Accepted'),
    ('C', 'Canceled'),
    ('R', 'Rejected'),
    ('W', 'Waiting')
]


class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=STATUS, default='W')
    booking_date = models.DateTimeField(blank=True, null=True)
    appointment_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.user.email + " - " + str(self.booking_date)


class ClinicAppointment(Appointment):
    schedule = models.ForeignKey(ClinicDetail, on_delete=models.CASCADE)


class RoomAppointment(Appointment):
    schedule = models.ForeignKey(RoomDetail, on_delete=models.CASCADE)


class ServiceAppointment(Appointment):
    schedule = models.ForeignKey(ServiceDetail, on_delete=models.CASCADE)
