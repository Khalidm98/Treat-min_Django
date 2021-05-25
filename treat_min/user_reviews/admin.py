from django.contrib import admin
from .models import ClinicReview, ServiceReview

REVIEW_FIELDS = ['user', 'date', 'rating', 'review']


class ClinicReviewAdmin(admin.ModelAdmin):
    fields = ['clinic'] + REVIEW_FIELDS
    readonly_fields = ['date']
    list_display = ['date', 'clinic', 'user', 'rating']


class ServiceReviewAdmin(admin.ModelAdmin):
    fields = ['service'] + REVIEW_FIELDS
    readonly_fields = ['date']
    list_display = ['date', 'service', 'user', 'rating']


admin.site.register(ClinicReview, ClinicReviewAdmin)
admin.site.register(ServiceReview, ServiceReviewAdmin)
