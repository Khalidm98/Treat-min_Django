from django.db import models
from ..accounts.models import User
from ..entities_details.models import ClinicDetail, RoomDetail, ServiceDetail

RATING = [('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')]


class Review(models.Model):
    date = models.DateField(auto_now_add=True)
    rating = models.CharField(max_length=1, choices=RATING)
    review = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        abstract = True


class ClinicReview(Review):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='clinics_reviews')
    clinic = models.ForeignKey(ClinicDetail, on_delete=models.CASCADE, related_name='reviews')

    class Meta:
        verbose_name_plural = 'Clinics Reviews'
        constraints = [
            models.UniqueConstraint(fields=['user', 'clinic'], name='unique_clinic_review')
        ]

    def __str__(self):
        return str(self.clinic) + " - " + self.user.user.email


class RoomReview(Review):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rooms_reviews')
    room = models.ForeignKey(RoomDetail, on_delete=models.CASCADE, related_name='reviews')

    class Meta:
        verbose_name_plural = 'Rooms Reviews'
        constraints = [
            models.UniqueConstraint(fields=['user', 'room'], name='unique_room_review')
        ]

    def __str__(self):
        return str(self.room) + " - " + self.user.user.email


class ServiceReview(Review):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='services_reviews')
    service = models.ForeignKey(ServiceDetail, on_delete=models.CASCADE, related_name='reviews')

    class Meta:
        verbose_name_plural = 'Services Reviews'
        constraints = [
            models.UniqueConstraint(fields=['user', 'service'], name='unique_service_review')
        ]

    def __str__(self):
        return str(self.service) + " - " + self.user.user.email
