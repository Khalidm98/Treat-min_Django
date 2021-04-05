from rest_framework import serializers
from ..models import *


class ClinicAppointmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = ClinicAppointment
        fields = ('id', 'booking_date', 'appointment_date', 'user', 'schedule')

class ClinicAppointmentStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = ClinicAppointment
        fields = ('id', 'booking_date', 'appointment_date', 'user', 'status')

