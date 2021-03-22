from django.db import models
from .details import ClinicDetail, RoomDetail, ServiceDetail

WEEK_DAYS = [
    ('SAT', 'Saturday'),
    ('SUN', 'Sunday'),
    ('MON', 'Monday'),
    ('TUE', 'Tuesday'),
    ('WED', 'Wednesday'),
    ('THU', 'Thursday'),
    ('FRI', 'Friday')
]


class Schedule(models.Model):
    day = models.CharField(max_length=3, choices=WEEK_DAYS)
    start = models.TimeField()
    end = models.TimeField()

    class Meta:
        abstract = True

    def __str__(self):
        return self.day + " (" + str(self.start) + " - " + str(self.end) + ")"


class ClinicSchedule(Schedule):
    clinic = models.ForeignKey(ClinicDetail, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.clinic) + " - " + super(ClinicSchedule, self).__str__()


class RoomSchedule(Schedule):
    room = models.ForeignKey(RoomDetail, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.room) + " - " + super(RoomSchedule, self).__str__()


class ServiceSchedule(Schedule):
    service = models.ForeignKey(ServiceDetail, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.service) + " - " + super(ServiceSchedule, self).__str__()
