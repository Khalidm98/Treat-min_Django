from django.db import models
from django.utils.translation import gettext_lazy as _
from ..accounts.models import User
from ..entities_details.models import ClinicDetail, RoomDetail, ServiceDetail

RATING = [('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')]


class Review(models.Model):
    date = models.DateField(auto_now=True, verbose_name=_('date'))
    rating = models.CharField(max_length=1, choices=RATING, verbose_name=_('rating'))
    review = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('review'))

    class Meta:
        abstract = True


class ClinicReview(Review):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='clinics_reviews', verbose_name=_('user'))
    clinic = models.ForeignKey(ClinicDetail, on_delete=models.CASCADE, related_name='reviews', verbose_name=_('clinic'))

    class Meta:
        verbose_name = _('clinic review')
        verbose_name_plural = _('Clinics Reviews')
        constraints = [
            models.UniqueConstraint(fields=['user', 'clinic'], name='unique_clinic_review')
        ]

    def __str__(self):
        return str(self.clinic) + " - " + self.user.user.email


class RoomReview(Review):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rooms_reviews', verbose_name=_('user'))
    room = models.ForeignKey(RoomDetail, on_delete=models.CASCADE, related_name='reviews', verbose_name=_('room'))

    class Meta:
        verbose_name = _('room review')
        verbose_name_plural = _('Rooms Reviews')
        constraints = [
            models.UniqueConstraint(fields=['user', 'room'], name='unique_room_review')
        ]

    def __str__(self):
        return str(self.room) + " - " + self.user.user.email


class ServiceReview(Review):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='services_reviews', verbose_name=_('user'))
    service = models.ForeignKey(
        ServiceDetail, on_delete=models.CASCADE, related_name='reviews', verbose_name=_('service')
    )

    class Meta:
        verbose_name = _('service review')
        verbose_name_plural = _('Services Reviews')
        constraints = [
            models.UniqueConstraint(fields=['user', 'service'], name='unique_service_review')
        ]

    def __str__(self):
        return str(self.service) + " - " + self.user.user.email
