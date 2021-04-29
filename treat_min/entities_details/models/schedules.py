from django.db import models
from django.utils.translation import gettext_lazy as _
from .details import ClinicDetail, RoomDetail, ServiceDetail

WEEK_DAYS = [
    ('SAT', _('Saturday')),
    ('SUN', _('Sunday')),
    ('MON', _('Monday')),
    ('TUE', _('Tuesday')),
    ('WED', _('Wednesday')),
    ('THU', _('Thursday')),
    ('FRI', _('Friday'))
]


class Schedule(models.Model):
    day = models.CharField(max_length=3, choices=WEEK_DAYS, verbose_name=_('day'))
    start = models.TimeField(verbose_name=_('start'))
    end = models.TimeField(verbose_name=_('end'))

    class Meta:
        abstract = True

    def __str__(self):
        return self.day + " (" + str(self.start) + " - " + str(self.end) + ")"


class ClinicSchedule(Schedule):
    clinic = models.ForeignKey(
        ClinicDetail, on_delete=models.CASCADE, related_name='schedules', verbose_name=_('clinic')
    )

    class Meta:
        verbose_name = _('clinic schedule')
        constraints = [
            models.UniqueConstraint(fields=['clinic', 'day', 'start', 'end'], name='unique_clinic_schedule')
        ]

    def __str__(self):
        return str(self.clinic) + " - " + super().__str__()


class RoomSchedule(Schedule):
    room = models.ForeignKey(RoomDetail, on_delete=models.CASCADE, related_name='schedules', verbose_name=_('room'))

    class Meta:
        verbose_name = _('room schedule')
        constraints = [
            models.UniqueConstraint(fields=['room', 'day', 'start', 'end'], name='unique_room_schedule')
        ]

    def __str__(self):
        return str(self.room) + " - " + super().__str__()


class ServiceSchedule(Schedule):
    service = models.ForeignKey(
        ServiceDetail, on_delete=models.CASCADE, related_name='schedules', verbose_name=_('service')
    )

    class Meta:
        verbose_name = _('service schedule')
        constraints = [
            models.UniqueConstraint(fields=['service', 'day', 'start', 'end'], name='unique_service_schedule')
        ]

    def __str__(self):
        return str(self.service) + " - " + super().__str__()
