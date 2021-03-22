# from collections import OrderedDict
from rest_framework import serializers
from ..models import *
# from ...accounts.models import *
from ...user_actions.models import *


DETAIL_FIELDS = ['id', 'hospital', 'price', 'rating_total', 'rating_users']
SCHEDULE_FIELDS = ['id', 'day', 'start', 'end']
REVIEW_FIELDS = ['date', 'rating', 'review']


class ClinicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clinic
        fields = '__all__'


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['name', 'title']


class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = ['name', 'address']


class ClinicDetailSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer()
    hospital = serializers.SlugRelatedField(read_only=True, slug_field='name')

    class Meta:
        model = ClinicDetail
        fields = DETAIL_FIELDS + ['doctor']

    # def to_representation(self, instance):
    #     result = super().to_representation(instance)
    #     print(result)
    #     return OrderedDict([(key, result[key]) for key in result if not result[key].schedule_set])


class ClinicScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClinicSchedule
        fields = SCHEDULE_FIELDS


class ClinicReviewSerializer(serializers.ModelSerializer):
    # add user.user.name

    class Meta:
        model = ClinicReview
        fields = REVIEW_FIELDS
