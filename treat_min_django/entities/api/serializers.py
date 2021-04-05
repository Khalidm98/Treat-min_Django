from rest_framework import serializers
from ...entities.models import Doctor
from ...user_appointments.models import *
from ...user_reviews.models import *

DETAIL_FIELDS = ['id', 'hospital', 'price', 'rating_total', 'rating_users']


class EntitySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=50)

    def create(self, validated_data):
        super().create(validated_data)

    def update(self, instance, validated_data):
        super().update(instance, validated_data)


class DoctorSerializer(serializers.ModelSerializer):
    # add photo
    class Meta:
        model = Doctor
        fields = ['name', 'title']


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


class ClinicAppointmentSerializer(serializers.ModelSerializer):
    schedule = ScheduleSerializer()
    hospital = serializers.SerializerMethodField('get_hospital')
    clinic = serializers.SerializerMethodField('get_clinic')
    doctor = serializers.SerializerMethodField('get_doctor')
    price = serializers.SerializerMethodField('get_price')

    def get_hospital(self, obj):
        return obj.schedule.clinic.hospital.name

    def get_clinic(self, obj):
        return obj.schedule.clinic.clinic.name

    def get_doctor(self, obj):
        return obj.schedule.clinic.doctor.name

    def get_price(self, obj):
        return obj.schedule.clinic.price

    class Meta:
        model = ClinicAppointment
        fields = ['hospital', 'clinic', 'doctor', 'price', 'schedule', 'status', 'appointment_date']


class RoomAppointmentSerializer(serializers.ModelSerializer):
    schedule = ScheduleSerializer()
    hospital = serializers.SerializerMethodField('get_hospital')
    room = serializers.SerializerMethodField('get_room')
    price = serializers.SerializerMethodField('get_price')

    def get_hospital(self, obj):
        return obj.schedule.room.hospital.name

    def get_room(self, obj):
        return obj.schedule.room.room.name

    def get_price(self, obj):
        return obj.schedule.room.price

    class Meta:
        model = RoomAppointment
        fields = ['hospital', 'room', 'price', 'schedule', 'status', 'appointment_date']


class ServiceAppointmentSerializer(serializers.ModelSerializer):
    schedule = ScheduleSerializer()
    hospital = serializers.SerializerMethodField('get_hospital')
    service = serializers.SerializerMethodField('get_service')
    price = serializers.SerializerMethodField('get_price')

    def get_hospital(self, obj):
        return obj.schedule.service.hospital.name

    def get_service(self, obj):
        return obj.schedule.service.service.name

    def get_price(self, obj):
        return obj.schedule.service.price

    class Meta:
        model = ServiceAppointment
        fields = ['hospital', 'service', 'price', 'schedule', 'status', 'appointment_date']


class ReviewSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField('get_name')

    def get_name(self, obj):
        return obj.user.user.name

    class Meta:
        model = ClinicReview
        fields = ['name', 'date', 'rating', 'review']
