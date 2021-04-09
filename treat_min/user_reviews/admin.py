from django.contrib import admin
from .models import ClinicReview, RoomReview, ServiceReview

REVIEW_FIELDS = ['user', 'date', 'rating', 'review']


class ClinicReviewAdmin(admin.ModelAdmin):
    fields = ['clinic'] + REVIEW_FIELDS
    readonly_fields = ['date']
    list_display = ['date', 'clinic', 'user', 'rating']


class RoomReviewAdmin(admin.ModelAdmin):
    fields = ['room'] + REVIEW_FIELDS
    readonly_fields = ['date']
    list_display = ['date', 'room', 'user', 'rating']


class ServiceReviewAdmin(admin.ModelAdmin):
    fields = ['service'] + REVIEW_FIELDS
    readonly_fields = ['date']
    list_display = ['date', 'service', 'user', 'rating']


admin.site.register(ClinicReview, ClinicReviewAdmin)
admin.site.register(RoomReview, RoomReviewAdmin)
admin.site.register(ServiceReview, ServiceReviewAdmin)
