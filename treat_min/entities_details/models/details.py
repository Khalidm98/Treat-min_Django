from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from ...entities.models import *


class Detail(models.Model):
    price = models.PositiveSmallIntegerField(default=50, verbose_name=_("price"))
    rating_total = models.PositiveIntegerField(default=0, verbose_name=_("rating_total"))
    rating_users = models.PositiveSmallIntegerField(default=0, verbose_name=_("rating_user"))

    class Meta:
        abstract = True


class ClinicDetail(Detail):
    hospital = models.ForeignKey(Hospital, on_delete=models.RESTRICT, related_name='clinics_details',
                                 verbose_name=_("hospital"))
    clinic = models.ForeignKey(Clinic, on_delete=models.RESTRICT, related_name='details', verbose_name=_("clinic"))
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='clinics_details',
                               verbose_name=_("doctor"))

    class Meta:
        verbose_name_plural = _('Clinics Details')
        verbose_name = _("clinic details")
        constraints = [
            models.UniqueConstraint(fields=['hospital', 'doctor', 'price'], name='unique_clinic_detail')
        ]

    def __str__(self):
        return self.hospital.name + " - " + self.clinic.name + " - " + self.doctor.name

    def clean(self):
        super().clean_fields()
        if self.doctor.speciality != self.clinic:
            raise ValidationError('Doctor\'s speciality and clinic speciality must match!')
        super().clean()


class RoomDetail(Detail):
    hospital = models.ForeignKey(Hospital, on_delete=models.RESTRICT, related_name='rooms_details',
                                 verbose_name=_("hospital"))
    room = models.ForeignKey(Room, on_delete=models.RESTRICT, related_name='details', verbose_name=_("room"))

    class Meta:
        verbose_name_plural = _('Rooms Details')
        verbose_name = _("room detail")
        constraints = [
            models.UniqueConstraint(fields=['hospital', 'room', 'price'], name='unique_room_detail')
        ]

    def __str__(self):
        return self.hospital.name + " - " + self.room.name


class ServiceDetail(Detail):
    hospital = models.ForeignKey(Hospital, on_delete=models.RESTRICT, related_name='services_details',
                                 verbose_name=_("hospital"))
    service = models.ForeignKey(Service, on_delete=models.RESTRICT, related_name='details', verbose_name=_("service"))

    class Meta:
        verbose_name_plural = _('Services Details')
        verbose_name = _("service details")
        constraints = [
            models.UniqueConstraint(fields=['hospital', 'service', 'price'], name='unique_service_detail')
        ]

    def __str__(self):
        return self.hospital.name + " - " + self.service.name