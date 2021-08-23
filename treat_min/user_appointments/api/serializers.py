from rest_framework import serializers
from ...entities_details.models import ClinicSchedule
from ..models import ClinicAppointment, ServiceAppointment

APPOINTMENT_FIELDS = ['id', 'entity', 'hospital', 'price', 'schedule', 'status', 'appointment_date']


class TimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClinicSchedule
        fields = ['start', 'end']


class ClinicAppointmentSerializer(serializers.ModelSerializer):
    hospital = serializers.SerializerMethodField('get_hospital')
    entity = serializers.SerializerMethodField('get_clinic')
    doctor = serializers.SerializerMethodField('get_doctor')
    price = serializers.SerializerMethodField('get_price')
    schedule = TimeSlotSerializer()

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
        fields = ['doctor'] + APPOINTMENT_FIELDS


class ServiceAppointmentSerializer(serializers.ModelSerializer):
    hospital = serializers.SerializerMethodField('get_hospital')
    entity = serializers.SerializerMethodField('get_service')
    price = serializers.SerializerMethodField('get_price')
    schedule = TimeSlotSerializer()

    def get_hospital(self, obj):
        return obj.schedule.service.hospital.name

    def get_service(self, obj):
        return obj.schedule.service.service.name

    def get_price(self, obj):
        return obj.schedule.service.price

    class Meta:
        model = ServiceAppointment
        fields = APPOINTMENT_FIELDS


class ClinicReserveSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClinicAppointment
        fields = ['appointment_date', 'schedule']


class ServiceReserveSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceAppointment
        fields = ['appointment_date', 'schedule']
