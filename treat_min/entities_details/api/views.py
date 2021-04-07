from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from ...entities.api.views import check_entity
from ..models import ClinicDetail, RoomDetail, ServiceDetail, ClinicSchedule, RoomSchedule, ServiceSchedule
from .serializers import ClinicDetailSerializer, RoomDetailSerializer, ServiceDetailSerializer, ScheduleSerializer


def check_detail(entities, entity_id, detail_id):
    result = check_entity(entities, entity_id)
    if isinstance(result, Response):
        return result

    try:
        if entities == 'clinics':
            detail = ClinicDetail.objects.get(id=detail_id)
            if detail.clinic.id != entity_id:
                return Response({"details": "Wrong clinic id!"}, status.HTTP_404_NOT_FOUND)

        elif entities == 'rooms':
            detail = RoomDetail.objects.get(id=detail_id)
            if detail.room.id != entity_id:
                return Response({"details": "Wrong room id!"}, status.HTTP_404_NOT_FOUND)

        else:
            detail = ServiceDetail.objects.get(id=detail_id)
            if detail.service.id != entity_id:
                return Response({"details": "Wrong service id!"}, status.HTTP_404_NOT_FOUND)

        return detail

    except ClinicDetail.DoesNotExist or RoomDetail.DoesNotExist or ServiceDetail.DoesNotExist:
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
            qs = ClinicDetail.objects.filter(clinic=entity_id)
            serializer = ClinicDetailSerializer(qs, many=True)
        elif entities == 'rooms':
            qs = RoomDetail.objects.filter(room=entity_id)
            serializer = RoomDetailSerializer(qs, many=True)
        else:
            qs = ServiceDetail.objects.filter(service=entity_id)
            serializer = ServiceDetailSerializer(qs, many=True)
        return Response({"details": serializer.data})


class ScheduleAPI(APIView):
    def get(self, request, entities, entity_id, detail_id):
        result = check_detail(entities, entity_id, detail_id)
        if isinstance(result, Response):
            return result

        if entities == 'clinics':
            qs = ClinicSchedule.objects.filter(clinic=detail_id)
        elif entities == 'rooms':
            qs = ServiceSchedule.objects.filter(service=detail_id)
        else:
            qs = RoomSchedule.objects.filter(room=detail_id)
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
