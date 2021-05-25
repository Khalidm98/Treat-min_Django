import os
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from ..filtration.models import City, Area

GENDER = [('M', _('Male')), ('F', _('Female'))]


def image_update(instance, filename):
    if isinstance(instance, Doctor):
        directory = 'photos/doctors/'
    elif isinstance(instance, Hospital):
        directory = 'photos/hospitals/'
    else:
        directory = 'photos/users/'

    if not instance.id:
        return directory + filename.split('.')[0] + '.png'

    path = directory + str(instance.id) + '.png'
    if os.path.exists('media/' + path):
        os.remove('media/' + path)
    return path


class Clinic(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name=_('name'))

    class Meta:
        ordering = ['name']
        verbose_name = _('clinic')
        verbose_name_plural = _('Clinics')

    def __str__(self):
        return self.name


class Service(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name=_('name'))

    class Meta:
        ordering = ['name']
        verbose_name = _('service')
        verbose_name_plural = _('Services')

    def __str__(self):
        return self.name


class Doctor(models.Model):
    name = models.CharField(max_length=50, verbose_name=_('name'))
    title = models.CharField(max_length=50, verbose_name=_('title'))
    gender = models.CharField(max_length=1, choices=GENDER, verbose_name=_('gender'))
    speciality = models.ForeignKey(
        Clinic, on_delete=models.CASCADE, related_name='doctors', verbose_name=_('speciality')
    )
    phone = models.CharField(max_length=11, unique=True, blank=True, null=True, verbose_name=_('phone'))
    photo = models.ImageField(upload_to=image_update, default='photos/default.png', verbose_name=_('photo'))

    class Meta:
        ordering = ['name']
        verbose_name = _('doctor')
        verbose_name_plural = _('Doctors')

    def __str__(self):
        return self.name


class Hospital(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name=_('name'))
    phone = models.CharField(max_length=11, verbose_name=_('phone'))
    address = models.CharField(max_length=100, verbose_name=_('address'))
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True, verbose_name=_('latitude'))
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True, verbose_name=_('longitude'))
    photo = models.ImageField(upload_to=image_update, default='photos/default.png', verbose_name=_('photo'))
    city = models.ForeignKey(
        City, on_delete=models.SET_NULL, related_name='hospitals', verbose_name=_('city'), null=True
    )
    area = models.ForeignKey(
        Area, on_delete=models.SET_NULL, related_name='hospitals', verbose_name=_('area'), null=True
    )
    doctors = models.ManyToManyField(
        Doctor, through='entities_details.ClinicDetail', related_name='hospitals', verbose_name=_('doctors')
    )
    clinics = models.ManyToManyField(
        Clinic, through='entities_details.ClinicDetail', related_name='hospitals', verbose_name=_('clinics')
    )
    services = models.ManyToManyField(
        Service, through='entities_details.ServiceDetail', related_name='hospitals', verbose_name=_('services')
    )

    class Meta:
        ordering = ['name']
        verbose_name = _('hospital')
        verbose_name_plural = _('Hospitals')

    def __str__(self):
        return self.name

    def clean(self):
        if hasattr(self, 'city') and hasattr(self, 'area'):
            if self.area:
                if self.city != self.area.city:
                    raise ValidationError(_('Area must be in the selected city!'))
