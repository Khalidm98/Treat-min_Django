from django.db import models
from django.core.exceptions import ValidationError
from treat_min_django.accounts.models import User
from treat_min_django.entities.models import ClinicDetail, RoomDetail, ServiceDetail


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    rating = models.PositiveSmallIntegerField()
    review = models.TextField(max_length=250)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if len(self.review) > 250:
            raise ValidationError('Reviews cannot contain more than 250 characters!')
        else:
            super().save(*args, **kwargs)


class ClinicReview(Review):
    clinic = models.ForeignKey(ClinicDetail, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Clinics Reviews'

    def __str__(self):
        return str(self.clinic) + " - " + self.user.user.email


class RoomReview(Review):
    room = models.ForeignKey(RoomDetail, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Rooms Reviews'

    def __str__(self):
        return str(self.room) + " - " + self.user.user.email


class ServiceReview(Review):
    service = models.ForeignKey(ServiceDetail, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Services Reviews'

    def __str__(self):
        return str(self.service) + " - " + self.user.user.email
