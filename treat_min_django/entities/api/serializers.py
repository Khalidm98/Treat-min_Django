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
    class Meta:
        model = ClinicAppointment
        # fields =


class ReviewSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField('get_name')

    def get_name(self, obj):
        return obj.user.user.name

    class Meta:
        model = ClinicReview
        fields = ['name', 'date', 'rating', 'review']


# class UpdateReviewSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ClinicReview
#         fields = ['rating', 'review']
