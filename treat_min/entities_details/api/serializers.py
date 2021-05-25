from rest_framework import serializers
from ...entities.models import Doctor, Hospital
from ..models import ClinicSchedule, ClinicDetail, ServiceDetail

DETAIL_FIELDS = ['id', 'hospital', 'price', 'rating_total', 'rating_users']


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['id', 'name', 'title']


class HospitalSerializer(serializers.ModelSerializer):
    area = serializers.SlugRelatedField(read_only=True, slug_field='name')
    city = serializers.SlugRelatedField(read_only=True, slug_field='name')

    class Meta:
        model = Hospital
        fields = ['id', 'name', 'phone', 'city', 'area']


class ClinicDetailSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer()
    hospital = HospitalSerializer()

    class Meta:
        model = ClinicDetail
        fields = DETAIL_FIELDS + ['doctor']


class ServiceDetailSerializer(serializers.ModelSerializer):
    hospital = HospitalSerializer()

    class Meta:
        model = ServiceDetail
        fields = DETAIL_FIELDS


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClinicSchedule
        fields = ['id', 'day', 'start', 'end']


class ClinicScheduleSerializer(ClinicDetailSerializer):
    schedules = ScheduleSerializer(many=True)

    class Meta:
        model = ClinicDetail
        fields = ClinicDetailSerializer.Meta.fields + ['schedules']


class ServiceScheduleSerializer(ServiceDetailSerializer):
    schedules = ScheduleSerializer(many=True)

    class Meta:
        model = ServiceDetail
        fields = ServiceDetailSerializer.Meta.fields + ['schedules']
