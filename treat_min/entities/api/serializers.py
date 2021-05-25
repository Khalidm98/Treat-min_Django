from rest_framework import serializers
from ..models import Clinic, Hospital


class EntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Clinic
        fields = '__all__'


class HospitalAPISerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = ['id', 'name']