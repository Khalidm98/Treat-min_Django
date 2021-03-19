from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from treat_min_django.treat_min.api.serializers import *


class ClinicList(APIView):
    def get(self, request):
        clinics = Clinic.objects.all()
        serializer = ClinicSerializer(clinics, many=True)
        return Response({'clinics': serializer.data})


class ClinicScheduleList(APIView):
    def get(self, request, clinic_id):
        try:
            schedules = ClinicDetail.objects.filter(clinic=clinic_id)
        except ClinicDetail.DoesNotExist:
            raise Http404
        serializer = ClinicScheduleSerializer(schedules, many=True)
        print()
        print(serializer.data[0])
        print()
        return Response({'schedules': serializer.data})


class ClinicBooking(APIView):
    def get(self, request, clinic_id, schedule_id):
        try:
            schedule = ClinicDetail.objects.get(id=schedule_id)
        except ClinicDetail.DoesNotExist:
            raise Http404
        if schedule.clinic.id != clinic_id:
            raise Http404
        serializer = ClinicBookingSerializer(schedule)
        return Response({'schedule': serializer.data})
