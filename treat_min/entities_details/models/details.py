from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from ...entities.models import Clinic, Room, Service, Doctor, Hospital


class Detail(models.Model):
    price = models.PositiveSmallIntegerField(default=50, verbose_name=_('price'))
    rating_total = models.PositiveIntegerField(default=0, verbose_name=_('rating total'))
    rating_users = models.PositiveSmallIntegerField(default=0, verbose_name=_('rating users'))

    class Meta:
        abstract = True


class ClinicDetail(Detail):
    hospital = models.ForeignKey(
        Hospital, on_delete=models.RESTRICT, related_name='clinics_details', verbose_name=_('hospital')
    )
    clinic = models.ForeignKey(Clinic, on_delete=models.RESTRICT, related_name='details', verbose_name=_('clinic'))
    doctor = models.ForeignKey(
        Doctor, on_delete=models.CASCADE, related_name='clinics_details', verbose_name=_('doctor')
    )

    class Meta:
        verbose_name = _('clinic details')
        verbose_name_plural = _('Clinics Details')
        constraints = [
            models.UniqueConstraint(fields=['hospital', 'doctor', 'price'], name='unique_clinic_detail')
        ]

    def __str__(self):
        return self.hospital.name + " - " + self.clinic.name + " - " + self.doctor.name

    def clean(self):
        if hasattr(self, 'doctor') and hasattr(self, 'clinic'):
            if self.doctor.speciality != self.clinic:
                raise ValidationError(_('Doctor\'s speciality and clinic speciality must match!'))


class RoomDetail(Detail):
    hospital = models.ForeignKey(
        Hospital, on_delete=models.RESTRICT, related_name='rooms_details', verbose_name=_('hospital')
    )
    room = models.ForeignKey(Room, on_delete=models.RESTRICT, related_name='details', verbose_name=_('room'))

    class Meta:
        verbose_name = _('room details')
        verbose_name_plural = _('Rooms Details')
        constraints = [
            models.UniqueConstraint(fields=['hospital', 'room', 'price'], name='unique_room_detail')
        ]

    def __str__(self):
        return self.hospital.name + " - " + self.room.name


class ServiceDetail(Detail):
    hospital = models.ForeignKey(
        Hospital, on_delete=models.RESTRICT, related_name='services_details', verbose_name=_('hospital')
    )
    service = models.ForeignKey(Service, on_delete=models.RESTRICT, related_name='details', verbose_name=_('service'))

    class Meta:
        verbose_name = _('service details')
        verbose_name_plural = _('Services Details')
        constraints = [
            models.UniqueConstraint(fields=['hospital', 'service', 'price'], name='unique_service_detail')
        ]

    def __str__(self):
        return self.hospital.name + " - " + self.service.name
