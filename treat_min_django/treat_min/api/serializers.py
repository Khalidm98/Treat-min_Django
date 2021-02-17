from rest_framework import serializers
from treat_min_django.treat_min.models import *


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


class ClinicScheduleSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer()
    hospital = serializers.SlugRelatedField(read_only=True, slug_field='name')

    class Meta:
        model = ClinicSchedule
        fields = ['id', 'hospital', 'price', 'doctor', 'day', 'time_from', 'time_to', ]


class ClinicBookingSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer()
    hospital = HospitalSerializer()

    class Meta:
        model = ClinicSchedule
        fields = ['id', 'hospital', 'price', 'doctor', 'day', 'time_from', 'time_to', ]
