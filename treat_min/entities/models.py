from django.db import models
from django.utils.translation import gettext_lazy as _

GENDER = [('M', _('Male')), ('F', _('Female'))]


class Clinic(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name=_('name'))

    class Meta:
        ordering = ['name']
        verbose_name_plural = _('Clinics')
        verbose_name = _('clinic')

    def __str__(self):
        return self.name


class Room(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name=_('name'))

    class Meta:
        ordering = ['name']
        verbose_name_plural = _('Rooms')
        verbose_name = _('room')

    def __str__(self):
        return self.name


class Service(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name=_('name'))

    class Meta:
        ordering = ['name']
        verbose_name_plural = _('Services')
        verbose_name = _('service')

    def __str__(self):
        return self.name


class Doctor(models.Model):
    name = models.CharField(max_length=50, verbose_name=_('name'))
    title = models.CharField(max_length=50, verbose_name=_('title'))
    gender = models.CharField(max_length=1, choices=GENDER, verbose_name=_('gender'))
    speciality = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name='doctors',
                                   verbose_name=_('speciality'))
    phone = models.CharField(max_length=11, blank=True, null=True, verbose_name=_('phone'))
    photo = models.ImageField(upload_to='photos/doctors/', blank=True, null=True, verbose_name=_('photo'))

    class Meta:
        ordering = ['name']
        verbose_name_plural = _('Doctors')
        verbose_name = _('doctor')

    def __str__(self):
        return self.name


class Hospital(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name=_('name'))
    phone = models.CharField(max_length=11, verbose_name=_('phone'))
    address = models.CharField(max_length=100, verbose_name=_('address'))
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True, verbose_name=_('latitude'))
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True, verbose_name=_('longitude'))
    photo = models.ImageField(upload_to='photos/hospitals/', blank=True, null=True, verbose_name=_('photo'))
    doctors = models.ManyToManyField(Doctor, through='entities_details.ClinicDetail', related_name='hospitals',
                                     verbose_name=_('doctors'))
    clinics = models.ManyToManyField(Clinic, through='entities_details.ClinicDetail', related_name='hospitals',
                                     verbose_name=_('clinics'))
    rooms = models.ManyToManyField(Room, through='entities_details.RoomDetail', related_name='hospitals',
                                   verbose_name=_('rooms'))
    services = models.ManyToManyField(Service, through='entities_details.ServiceDetail', related_name='hospitals',
                                      verbose_name=_('services'))

    class Meta:
        ordering = ['name']
        verbose_name_plural = _('Hospitals')
        verbose_name = _('Hospital')

    def __str__(self):
        return self.name