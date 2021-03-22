from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *


class ClinicList(APIView):
    def get(self, request):
        clinics = Clinic.objects.all()
        serializer = ClinicSerializer(clinics, many=True)
        return Response({'clinics': serializer.data})


class ClinicDetailList(APIView):
    def get(self, request, clinic_id):
        try:
            details = ClinicDetail.objects.filter(clinic=clinic_id)
        except ClinicDetail.DoesNotExist:
            raise Http404
        serializer = ClinicDetailSerializer(details, many=True)
        return Response({'details': serializer.data})


class ClinicDetailSchedules(APIView):
    def get(self, request, clinic_id, detail_id):
        try:
            detail = ClinicDetail.objects.get(id=detail_id)
        except ClinicDetail.DoesNotExist:
            raise Http404
        if detail.clinic.id != clinic_id:
            raise Http404
        schedules = ClinicSchedule.objects.filter(clinic=detail_id)
        serializer = ClinicScheduleSerializer(schedules, many=True)
        return Response({
            'doctor': detail.doctor.name,
            'title': detail.doctor.title,
            'hospital': detail.hospital.name,
            'address': detail.hospital.address,
            'schedules': serializer.data
        })


class ClinicReviewsList(APIView):
    def get(self, request, clinic_id, detail_id):
        try:
            detail = ClinicDetail.objects.get(id=detail_id)
        except ClinicDetail.DoesNotExist:
            raise Http404
        if detail.clinic.id != clinic_id:
            raise Http404
        reviews = ClinicReview.objects.filter(clinic=detail_id)
        serializer = ClinicReviewSerializer(reviews, many=True)
        return Response({'reviews': serializer.data})
