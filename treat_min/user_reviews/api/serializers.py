from rest_framework import serializers
from ..models import ClinicReview


class ReviewSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField('get_name')

    def get_name(self, obj):
        return obj.user.user.name

    class Meta:
        model = ClinicReview
        fields = ['name', 'date', 'rating', 'review']


class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClinicReview
        fields = ['rating', 'review']
