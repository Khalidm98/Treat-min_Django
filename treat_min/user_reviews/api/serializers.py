from rest_framework import serializers
from ..models import ClinicReview


class ReviewSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField('get_name')
    user_id = serializers.SerializerMethodField('get_user_id')

    def get_name(self, obj):
        return obj.user.user.name

    def get_user_id(self, obj):
        return obj.user.id

    class Meta:
        model = ClinicReview
        fields = ['user_id', 'name', 'date', 'rating', 'review']


class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClinicReview
        fields = ['rating', 'review']
