import abc
from rest_framework import serializers
from ...entities_details.models import ClinicSchedule
from ..models import ClinicAppointment, RoomAppointment, ServiceAppointment


class TimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClinicSchedule
        fields = ['start', 'end']


class AppointmentSerializer(serializers.ModelSerializer):
    schedule = TimeSlotSerializer()
    hospital = serializers.SerializerMethodField('get_hospital')
    price = serializers.SerializerMethodField('get_price')

    @abc.abstractmethod
    def get_detail(self, obj):
        pass

    def get_hospital(self, obj):
        return self.get_detail(obj).hospital.name

    def get_price(self, obj):
        return self.get_detail(obj).price

    class Meta:
        abstract = True
        fields = ['hospital', 'price', 'schedule', 'status', 'appointment_date']


class ClinicAppointmentSerializer(AppointmentSerializer):
    clinic = serializers.SerializerMethodField('get_clinic')
    doctor = serializers.SerializerMethodField('get_doctor')

    def get_detail(self, obj):
        return obj.schedule.clinic

    def get_clinic(self, obj):
        return self.get_detail(obj).clinic.name

    def get_doctor(self, obj):
        return self.get_detail(obj).doctor.name

    class Meta:
        model = ClinicAppointment
        fields = ['doctor', 'clinic'] + AppointmentSerializer.Meta.fields


class RoomAppointmentSerializer(AppointmentSerializer):
    room = serializers.SerializerMethodField('get_room')

    def get_detail(self, obj):
        return obj.schedule.room

    def get_room(self, obj):
        return self.get_detail(obj).room.name

    class Meta:
        model = RoomAppointment
        fields = ['room'] + AppointmentSerializer.Meta.fields


class ServiceAppointmentSerializer(AppointmentSerializer):
    service = serializers.SerializerMethodField('get_service')

    def get_detail(self, obj):
        return obj.schedule.service

    def get_service(self, obj):
        return self.get_detail(obj).service.name

    class Meta:
        model = ServiceAppointment
        fields = ['service'] + AppointmentSerializer.Meta.fields


class ReserveSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClinicAppointment
        fields = ['appointment_date', 'schedule']
