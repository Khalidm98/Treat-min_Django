from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from ...entities.api.views import check_entity
from ..models import ClinicDetail, ServiceDetail, ClinicSchedule, ServiceSchedule
from .serializers import ClinicDetailSerializer, ServiceDetailSerializer, ScheduleSerializer, \
    ClinicScheduleSerializer, ServiceScheduleSerializer


def check_detail(entities, entity_id, detail_id):
    result = check_entity(entities, entity_id)
    if isinstance(result, Response):
        return result

    try:
        if entities == 'clinics':
            detail = ClinicDetail.objects.get(id=detail_id)
            if detail.clinic.id != entity_id:
                return Response({"details": "Wrong clinic id!"}, status.HTTP_404_NOT_FOUND)

        else:
            detail = ServiceDetail.objects.get(id=detail_id)
            if detail.service.id != entity_id:
                return Response({"details": "Wrong service id!"}, status.HTTP_404_NOT_FOUND)

        return detail

    except (ClinicDetail.DoesNotExist, ServiceDetail.DoesNotExist):
        return Response(
            {"details": "{0} detail not found!".format(entities[0:len(entities) - 1])},
            status.HTTP_404_NOT_FOUND
        )


class DetailAPI(APIView):
    def get(self, request, entities, entity_id):
        result = check_entity(entities, entity_id)
        if isinstance(result, Response):
            return result

        if entities == 'clinics':
            qs = ClinicDetail.objects.filter(clinic=entity_id, schedules__isnull=False).distinct()
            serializer = ClinicDetailSerializer(qs, many=True)
        else:
            qs = ServiceDetail.objects.filter(service=entity_id, schedules__isnull=False).distinct()
            serializer = ServiceDetailSerializer(qs, many=True)
        return Response(
            {
                "entity": result.name,
                "details": serializer.data
            }
        )


class ScheduleAPI(APIView):
    def get(self, request, entities, entity_id, detail_id):
        result = check_detail(entities, entity_id, detail_id)
        if isinstance(result, Response):
            return result

        if entities == 'clinics':
            qs = ClinicSchedule.objects.filter(clinic=detail_id)
        else:
            qs = ServiceSchedule.objects.filter(service=detail_id)
        serializer = ScheduleSerializer(qs, many=True)

        if entities == 'clinics':
            return Response({
                "doctor": result.doctor.name,
                "title": result.doctor.title,
                "hospital": result.hospital.name,
                "address": result.hospital.address,
                "schedules": serializer.data
            })
        else:
            return Response({
                "hospital": result.hospital.name,
                "address": result.hospital.address,
                "schedules": serializer.data
            })


class WebSchedulesAPI(APIView):
    def get(self, request, entities, entity_id):
        result = check_entity(entities, entity_id)
        if isinstance(result, Response):
            return result

        if entities == 'clinics':
            qs = ClinicDetail.objects.filter(clinic=entity_id, schedules__isnull=False).distinct()
            serializer = ClinicScheduleSerializer(qs, many=True)
        else:
            qs = ServiceDetail.objects.filter(service=entity_id, schedules__isnull=False).distinct()
            serializer = ServiceScheduleSerializer(qs, many=True)
        return Response(
            {
                "entity": result.name,
                "details": serializer.data
            }
        )
