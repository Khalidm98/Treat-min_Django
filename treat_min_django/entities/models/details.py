from django.core.exceptions import ValidationError
from .entities import *


class Detail(models.Model):
    price = models.PositiveSmallIntegerField(default=50)
    rating_total = models.PositiveIntegerField(default=0)
    rating_users = models.PositiveSmallIntegerField(default=0)

    class Meta:
        abstract = True


class ClinicDetail(Detail):
    hospital = models.ForeignKey(Hospital, on_delete=models.RESTRICT, related_name='clinics_details')
    clinic = models.ForeignKey(Clinic, on_delete=models.RESTRICT, related_name='details')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='clinics_details')

    class Meta:
        verbose_name_plural = 'Clinics Details'
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
    hospital = models.ForeignKey(Hospital, on_delete=models.RESTRICT, related_name='rooms_details')
    room = models.ForeignKey(Room, on_delete=models.RESTRICT, related_name='details')

    class Meta:
        verbose_name_plural = 'Rooms Details'
        constraints = [
            models.UniqueConstraint(fields=['hospital', 'room', 'price'], name='unique_room_detail')
        ]

    def __str__(self):
        return self.hospital.name + " - " + self.room.name


class ServiceDetail(Detail):
    hospital = models.ForeignKey(Hospital, on_delete=models.RESTRICT, related_name='services_details')
    service = models.ForeignKey(Service, on_delete=models.RESTRICT, related_name='details')

    class Meta:
        verbose_name_plural = 'Services Details'
        constraints = [
            models.UniqueConstraint(fields=['hospital', 'service', 'price'], name='unique_service_detail')
        ]

    def __str__(self):
        return self.hospital.name + " - " + self.service.name
