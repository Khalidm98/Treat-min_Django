from rest_framework import serializers
from ...entities_details.models import ClinicSchedule
from ..models import ClinicAppointment, RoomAppointment, ServiceAppointment

APPOINTMENT_FIELDS = ['hospital', 'price', 'schedule', 'status', 'appointment_date']


class TimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClinicSchedule
        fields = ['start', 'end']


class ClinicAppointmentSerializer(serializers.ModelSerializer):
    hospital = serializers.SerializerMethodField('get_hospital')
    clinic = serializers.SerializerMethodField('get_clinic')
    doctor = serializers.SerializerMethodField('get_doctor')
    price = serializers.SerializerMethodField('get_price')
    clinic_id = serializers.SerializerMethodField('get_clinic_id')
    clinic_detail_id = serializers.SerializerMethodField('get_clinic_detail_id')
    schedule = TimeSlotSerializer()

    def get_hospital(self, obj):
        return obj.schedule.clinic.hospital.name

    def get_clinic(self, obj):
        return obj.schedule.clinic.clinic.name

    def get_clinic_detail_id(self, obj):
        return obj.schedule.clinic.id

    def get_clinic_id(self, obj):
        return obj.schedule.clinic.clinic.id

    def get_doctor(self, obj):
        return obj.schedule.clinic.doctor.name

    def get_price(self, obj):
        return obj.schedule.clinic.price

    class Meta:
        model = ClinicAppointment
        fields = ['id', 'doctor', 'clinic_id', 'clinic', 'clinic_detail_id'] + APPOINTMENT_FIELDS


class RoomAppointmentSerializer(serializers.ModelSerializer):
    hospital = serializers.SerializerMethodField('get_hospital')
    room = serializers.SerializerMethodField('get_room')
    room_id = serializers.SerializerMethodField('get_room_id')
    room_detail_id = serializers.SerializerMethodField('get_room_detail_id')
    price = serializers.SerializerMethodField('get_price')
    schedule = TimeSlotSerializer()

    def get_hospital(self, obj):
        return obj.schedule.room.hospital.name

    def get_room(self, obj):
        return obj.schedule.room.room.name

    def get_room_detail_id(self, obj):
        return obj.schedule.room.id

    def get_room_id(self, obj):
        return obj.schedule.room.room.id

    def get_price(self, obj):
        return obj.schedule.room.price

    class Meta:
        model = RoomAppointment
        fields = ['id', 'room_id', 'room', 'room_detail_id'] + APPOINTMENT_FIELDS


class ServiceAppointmentSerializer(serializers.ModelSerializer):
    hospital = serializers.SerializerMethodField('get_hospital')
    service = serializers.SerializerMethodField('get_service')
    service_id = serializers.SerializerMethodField('get_service_id')
    service_detail_id = serializers.SerializerMethodField('get_service_detail_id')
    price = serializers.SerializerMethodField('get_price')
    schedule = TimeSlotSerializer()

    def get_hospital(self, obj):
        return obj.schedule.service.hospital.name

    def get_service(self, obj):
        return obj.schedule.service.service.name

    def get_service_detail_id(self, obj):
        return obj.schedule.service.id

    def get_service_id(self, obj):
        return obj.schedule.service.service.id

    def get_price(self, obj):
        return obj.schedule.service.price

    class Meta:
        model = ServiceAppointment
        fields = ['id', 'service_id', 'service', 'service_detail_id'] + APPOINTMENT_FIELDS


class ClinicReserveSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClinicAppointment
        fields = ['appointment_date', 'schedule']


class RoomReserveSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomAppointment
        fields = ['appointment_date', 'schedule']


class ServiceReserveSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceAppointment
        fields = ['appointment_date', 'schedule']
