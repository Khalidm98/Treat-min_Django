from collections import OrderedDict
from rest_framework import serializers
from treat_min_django.entities.models import *


DETAIL_FIELDS = [
    'hospital', 'price', 'rating_total', 'rating_users',
    'sat_from', 'sat_to', 'sun_from', 'sun_to', 'mon_from', 'mon_to',
    'tue_from', 'tue_to', 'wed_from', 'wed_to', 'thu_from', 'thu_to', 'fri_from', 'fri_to'
]


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
    sun_from = serializers.TimeField(required=False)

    class Meta:
        model = ClinicDetail
        fields = ['id', 'doctor'] + DETAIL_FIELDS

    def to_representation(self, instance):
        result = super(ClinicDetailSerializer, self).to_representation(instance)
        return OrderedDict([(key, result[key]) for key in result if result[key] is not None])


class ClinicBookingSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer()
    hospital = HospitalSerializer()

    class Meta:
        model = ClinicDetail
        fields = ['id', 'doctor'] + DETAIL_FIELDS

    def to_representation(self, instance):
        result = super(ClinicBookingSerializer, self).to_representation(instance)
        return OrderedDict([(key, result[key]) for key in result if result[key] is not None])
