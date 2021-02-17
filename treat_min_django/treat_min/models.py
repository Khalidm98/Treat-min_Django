# list of schedules
# rating_total, rating_users

from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db import models

GENDER = (('M', 'Male'), ('F', 'Female'),)

WEEK_DAYS = (
    ('Sat', 'Saturday'),
    ('Sun', 'Sunday'),
    ('Mon', 'Monday'),
    ('Tue', 'Tuesday'),
    ('Wed', 'Wednesday'),
    ('Thu', 'Thursday'),
    ('Fri', 'Friday'),
)

STATUS = (
    ('Accepted', 'Accepted'),
    ('Canceled', 'Canceled'),
    ('Rejected', 'Rejected'),
    ('Waiting', 'Waiting'),
)


class Clinic(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Room(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Service(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Doctor(models.Model):
    name = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    gender = models.CharField(max_length=1, choices=GENDER)
    speciality = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    phone = models.CharField(max_length=11, blank=True, null=True)

    # photo = models.ImageField(blank=True, null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Hospital(models.Model):
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=11)
    address = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    doctors = models.ManyToManyField(Doctor, through='ClinicSchedule')
    clinics = models.ManyToManyField(Clinic, through='ClinicSchedule')
    rooms = models.ManyToManyField(Room, through='RoomSchedule')
    services = models.ManyToManyField(Service, through='ServiceSchedule')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Schedule(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    price = models.PositiveSmallIntegerField(default=50)
    sat_from = models.TimeField(blank=True, null=True)
    sat_to = models.TimeField(blank=True, null=True)
    sun_from = models.TimeField(blank=True, null=True)
    sun_to = models.TimeField(blank=True, null=True)
    mon_from = models.TimeField(blank=True, null=True)
    mon_to = models.TimeField(blank=True, null=True)
    tue_from = models.TimeField(blank=True, null=True)
    tue_to = models.TimeField(blank=True, null=True)
    wed_from = models.TimeField(blank=True, null=True)
    wed_to = models.TimeField(blank=True, null=True)
    thu_from = models.TimeField(blank=True, null=True)
    thu_to = models.TimeField(blank=True, null=True)
    fri_from = models.TimeField(blank=True, null=True)
    fri_to = models.TimeField(blank=True, null=True)

    class Meta:
        abstract = True

    def clean(self):
        from_all = (self.sat_from or self.sun_from or self.mon_from or
                    self.tue_from or self.wed_from or self.thu_from or self.fri_from)
        to_all = self.sat_to or self.sun_to or self.mon_to or self.tue_to or self.wed_to or self.thu_to or self.fri_to
        if not from_all and not to_all:
            raise ValidationError('You must determine at least one schedule!')
        elif (self.sat_from and not self.sat_to) or (not self.sat_from and self.sat_to):
            raise ValidationError('Saturday schedule is incorrect!')
        elif (self.sun_from and not self.sun_to) or (not self.sun_from and self.sun_to):
            raise ValidationError('Sunday schedule is incorrect!')
        elif (self.mon_from and not self.mon_to) or (not self.mon_from and self.mon_to):
            raise ValidationError('Monday schedule is incorrect!')
        elif (self.tue_from and not self.tue_to) or (not self.tue_from and self.tue_to):
            raise ValidationError('Tuesday schedule is incorrect!')
        elif (self.wed_from and not self.wed_to) or (not self.wed_from and self.wed_to):
            raise ValidationError('Wednesday schedule is incorrect!')
        elif (self.thu_from and not self.thu_to) or (not self.thu_from and self.thu_to):
            raise ValidationError('Thursday schedule is incorrect!')
        elif (self.fri_from and not self.fri_to) or (not self.fri_from and self.fri_to):
            raise ValidationError('Friday schedule is incorrect!')
        super(Schedule, self).clean()


class ClinicSchedule(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    price = models.PositiveSmallIntegerField(default=50)
    day = models.CharField(max_length=3, choices=WEEK_DAYS)
    time_from = models.TimeField()
    time_to = models.TimeField()

    def __str__(self):
        return self.hospital.name + " - " + self.clinic.name + " - " + self.doctor.name

    def clean(self):
        if self.doctor.speciality != self.clinic:
            raise ValidationError('Doctor\'s speciality and clinic speciality must match!')
        super(ClinicSchedule, self).clean()


class RoomSchedule(Schedule):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    def __str__(self):
        return self.hospital.name + " - " + self.room.name


class ServiceSchedule(Schedule):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    def __str__(self):
        return self.hospital.name + " - " + self.service.name


class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=8, choices=STATUS, default='Waiting')
    booking_date = models.DateTimeField(blank=True, null=True)
    appointment_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.user.username + " - " + str(self.booking_date)


class ClinicAppointment(Appointment):
    schedule = models.ForeignKey(ClinicSchedule, on_delete=models.CASCADE)


class RoomAppointment(Appointment):
    schedule = models.ForeignKey(RoomSchedule, on_delete=models.CASCADE)


class ServiceAppointment(Appointment):
    schedule = models.ForeignKey(ServiceSchedule, on_delete=models.CASCADE)
