from django.db import models

GENDER = [('M', 'Male'), ('F', 'Female')]


class Entity(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        abstract = True
        ordering = ['name']

    def __str__(self):
        return self.name


class Clinic(Entity):
    pass


class Room(Entity):
    pass


class Service(Entity):
    pass


class Doctor(Entity):
    name = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    gender = models.CharField(max_length=1, choices=GENDER)
    speciality = models.ForeignKey(Clinic, on_delete=models.RESTRICT, related_name='doctors')
    phone = models.CharField(max_length=11, blank=True, null=True)
    photo = models.ImageField(upload_to='photos/doctors/', blank=True, null=True)


class Hospital(Entity):
    phone = models.CharField(max_length=11)
    address = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    photo = models.ImageField(upload_to='photos/hospitals/', blank=True, null=True)
    doctors = models.ManyToManyField(Doctor, through='entities_details.ClinicDetail', related_name='hospitals')
    clinics = models.ManyToManyField(Clinic, through='entities_details.ClinicDetail', related_name='hospitals')
    rooms = models.ManyToManyField(Room, through='entities_details.RoomDetail', related_name='hospitals')
    services = models.ManyToManyField(Service, through='entities_details.ServiceDetail', related_name='hospitals')
