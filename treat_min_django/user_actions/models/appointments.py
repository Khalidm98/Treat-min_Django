from django.db import models
from treat_min_django.accounts.models import User
from treat_min_django.entities.models import ClinicSchedule, RoomSchedule, ServiceSchedule

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


class RoomAppointment(Appointment):
    schedule = models.ForeignKey(RoomSchedule, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name_plural = 'Rooms Appointments'


class ServiceAppointment(Appointment):
    schedule = models.ForeignKey(ServiceSchedule, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name_plural = 'Services Appointments'
