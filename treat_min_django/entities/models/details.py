from django.core.exceptions import ValidationError
from .entities import *


class Detail(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.RESTRICT)
    price = models.PositiveSmallIntegerField(default=50)
    rating_total = models.PositiveIntegerField(default=0)
    rating_users = models.PositiveSmallIntegerField(default=0)

    class Meta:
        abstract = True


class ClinicDetail(Detail):
    clinic = models.ForeignKey(Clinic, on_delete=models.RESTRICT)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Clinics Details'

    def __str__(self):
        return self.hospital.name + " - " + self.clinic.name + " - " + self.doctor.name

    def clean(self):
        if self.doctor.speciality != self.clinic:
            raise ValidationError('Doctor\'s speciality and clinic speciality must match!')
        super().clean()


class RoomDetail(Detail):
    room = models.ForeignKey(Room, on_delete=models.RESTRICT)

    class Meta:
        verbose_name_plural = 'Rooms Details'

    def __str__(self):
        return self.hospital.name + " - " + self.room.name


class ServiceDetail(Detail):
    service = models.ForeignKey(Service, on_delete=models.RESTRICT)

    class Meta:
        verbose_name_plural = 'Services Details'

    def __str__(self):
        return self.hospital.name + " - " + self.service.name
