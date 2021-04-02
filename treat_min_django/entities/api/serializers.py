from rest_framework import serializers
from ...entities.models import *
from ...user_appointments.models import *
from ...user_reviews.models import *


DETAIL_FIELDS = ['id', 'hospital', 'price', 'rating_total', 'rating_users']
SCHEDULE_FIELDS = ['id', 'day', 'start', 'end']
REVIEW_FIELDS = ['name', 'date', 'rating', 'review']


class ClinicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clinic
        fields = '__all__'


class DoctorSerializer(serializers.ModelSerializer):
    # add photo
    class Meta:
        model = Doctor
        fields = ['name', 'title']


class HospitalSerializer(serializers.ModelSerializer):
    # add photo
    class Meta:
        model = Hospital
        fields = ['name', 'address']


class ClinicDetailSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer()
    hospital = serializers.SlugRelatedField(read_only=True, slug_field='name')

    class Meta:
        model = ClinicDetail
        fields = DETAIL_FIELDS + ['doctor']


class ClinicScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClinicSchedule
        fields = SCHEDULE_FIELDS


class ClinicAppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClinicAppointment
        # fields =


class ClinicReviewSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField('get_name')

    def get_name(self, obj):
        return obj.user.user.name

    class Meta:
        model = ClinicReview
        fields = REVIEW_FIELDS
