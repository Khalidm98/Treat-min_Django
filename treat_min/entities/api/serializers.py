from rest_framework import serializers
from ..models import Clinic


class EntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Clinic
        fields = '__all__'
