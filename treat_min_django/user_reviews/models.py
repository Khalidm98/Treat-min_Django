from django.db import models
from django.core.exceptions import ValidationError
from treat_min_django.accounts.models import User
from treat_min_django.entities_details.models import ClinicDetail, RoomDetail, ServiceDetail


class Review(models.Model):
    date = models.DateField(auto_now_add=True)
    rating = models.PositiveSmallIntegerField()
    review = models.TextField(max_length=250, blank=True, null=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if len(self.review) > 250:
            raise ValidationError('Reviews cannot contain more than 250 characters!')
        else:
            super().save(*args, **kwargs)


class ClinicReview(Review):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='clinics_reviews')
    clinic = models.ForeignKey(ClinicDetail, on_delete=models.CASCADE, related_name='reviews')

    class Meta:
        verbose_name_plural = 'Clinics Reviews'

    def __str__(self):
        return str(self.clinic) + " - " + self.user.user.email


class RoomReview(Review):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rooms_reviews')
    room = models.ForeignKey(RoomDetail, on_delete=models.CASCADE, related_name='reviews')

    class Meta:
        verbose_name_plural = 'Rooms Reviews'

    def __str__(self):
        return str(self.room) + " - " + self.user.user.email


class ServiceReview(Review):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='services_reviews')
    service = models.ForeignKey(ServiceDetail, on_delete=models.CASCADE, related_name='reviews')

    class Meta:
        verbose_name_plural = 'Services Reviews'

    def __str__(self):
        return str(self.service) + " - " + self.user.user.email
