from rest_framework import serializers
from ...entities.models import Doctor
from ..models import ClinicSchedule, ClinicDetail, RoomDetail, ServiceDetail

DETAIL_FIELDS = ['id', 'hospital', 'price', 'rating_total', 'rating_users']


class DoctorSerializer(serializers.ModelSerializer):
    # add photo
    class Meta:
        model = Doctor
        fields = ['id', 'name', 'title']


class ClinicDetailSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer()
    hospital = serializers.SlugRelatedField(read_only=True, slug_field='name')

    class Meta:
        model = ClinicDetail
        fields = DETAIL_FIELDS + ['doctor']


class RoomDetailSerializer(serializers.ModelSerializer):
    hospital = serializers.SlugRelatedField(read_only=True, slug_field='name')

    class Meta:
        model = RoomDetail
        fields = DETAIL_FIELDS


class ServiceDetailSerializer(serializers.ModelSerializer):
    hospital = serializers.SlugRelatedField(read_only=True, slug_field='name')

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


class RoomScheduleSerializer(RoomDetailSerializer):
    schedules = ScheduleSerializer(many=True)

    class Meta:
        model = RoomDetail
        fields = RoomDetailSerializer.Meta.fields + ['schedules']


class ServiceScheduleSerializer(ServiceDetailSerializer):
    schedules = ScheduleSerializer(many=True)

    class Meta:
        model = ServiceDetail
        fields = ServiceDetailSerializer.Meta.fields + ['schedules']
