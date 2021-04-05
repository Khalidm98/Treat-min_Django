from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from knox.auth import TokenAuthentication
from knox.models import AuthToken

from . import serializers
from .. import models
from ...entities_details import models as details
from ...user_reviews import models as reviews


class EntityAPI(APIView):
    def get(self, request, entities):
        if entities == 'clinics':
            qs = models.Clinic.objects.all()
        elif entities == 'rooms':
            qs = models.Room.objects.all()
        elif entities == 'services':
            qs = models.Service.objects.all()
        else:
            return Response({"details": "Page not found!"}, status.HTTP_404_NOT_FOUND)
        serializer = serializers.EntitySerializer(qs, many=True)
        return Response({entities: serializer.data})


class DetailAPI(APIView):
    def get(self, request, entities, entity_id):
        if entities == 'clinics':
            qs = details.ClinicDetail.objects.filter(clinic=entity_id)
            serializer = serializers.ClinicDetailSerializer(qs, many=True)
        elif entities == 'rooms':
            qs = details.RoomDetail.objects.filter(room=entity_id)
            serializer = serializers.RoomDetailSerializer(qs, many=True)
        elif entities == 'services':
            qs = details.ServiceDetail.objects.filter(service=entity_id)
            serializer = serializers.ServiceDetailSerializer(qs, many=True)
        else:
            return Response({"details": "Page not found!"}, status.HTTP_404_NOT_FOUND)
        return Response({"details": serializer.data})


class ScheduleAPI(APIView):
    def get(self, request, entities, entity_id, detail_id):
        try:
            if entities == 'clinics':
                detail = details.ClinicDetail.objects.get(id=detail_id)
                if detail.clinic.id != entity_id:
                    return Response({"details": "Wrong clinic id!"}, status.HTTP_404_NOT_FOUND)
                qs = details.ClinicSchedule.objects.filter(clinic=detail_id)

            elif entities == 'rooms':
                detail = details.RoomDetail.objects.get(id=detail_id)
                if detail.room.id != entity_id:
                    return Response({"details": "Wrong room id!"}, status.HTTP_404_NOT_FOUND)
                qs = details.RoomSchedule.objects.filter(room=detail_id)

            elif entities == 'services':
                detail = details.ServiceDetail.objects.get(id=detail_id)
                if detail.service.id != entity_id:
                    return Response({"details": "Wrong service id!"}, status.HTTP_404_NOT_FOUND)
                qs = details.ServiceSchedule.objects.filter(service=detail_id)

            else:
                return Response({"details": "Page not found!"}, status.HTTP_404_NOT_FOUND)

        except details.ClinicDetail.DoesNotExist \
            or details.RoomDetail.DoesNotExist \
                or details.ServiceDetail.DoesNotExist:
            return Response(
                {"details": "{0} detail not found!".format(entities[0:len(entities) - 1])},
                status.HTTP_404_NOT_FOUND
            )

        serializer = serializers.ScheduleSerializer(qs, many=True)
        if entities == 'clinics':
            return Response({
                "doctor": detail.doctor.name,
                "title": detail.doctor.title,
                "hospital": detail.hospital.name,
                "address": detail.hospital.address,
                "schedules": serializer.data
            })
        else:
            return Response({
                "hospital": detail.hospital.name,
                "address": detail.hospital.address,
                "schedules": serializer.data
            })


class AppointmentAPI(APIView):
    def get(self, request, clinic_id, detail_id):
        pass

    def post(self, request, clinic_id, detail_id):
        pass


class ReviewAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def check_detail(self, entities, entity_id, detail_id):
        try:
            if entities == 'clinics':
                detail = details.ClinicDetail.objects.get(id=detail_id)
                if detail.clinic.id != entity_id:
                    return Response({"details": "Wrong clinic id!"}, status.HTTP_404_NOT_FOUND)

            elif entities == 'rooms':
                detail = details.RoomDetail.objects.get(id=detail_id)
                if detail.room.id != entity_id:
                    return Response({"details": "Wrong room id!"}, status.HTTP_404_NOT_FOUND)

            elif entities == 'services':
                detail = details.ServiceDetail.objects.get(id=detail_id)
                if detail.service.id != entity_id:
                    return Response({"details": "Wrong service id!"}, status.HTTP_404_NOT_FOUND)

            else:
                return Response({"details": "Page not found!"}, status.HTTP_404_NOT_FOUND)

        except details.ClinicDetail.DoesNotExist \
            or details.RoomDetail.DoesNotExist \
                or details.ServiceDetail.DoesNotExist:
            return Response(
                {"details": "{0} detail not found!".format(entities[0:len(entities) - 1])},
                status.HTTP_404_NOT_FOUND
            )

    def get(self, request, entities, entity_id, detail_id):
        response = self.check_detail(entities, entity_id, detail_id)
        if response:
            return response

        if entities == 'clinics':
            qs = reviews.ClinicReview.objects.filter(clinic=detail_id)
        elif entities == 'rooms':
            qs = reviews.RoomReview.objects.filter(room=detail_id)
        else:
            qs = reviews.ServiceReview.objects.filter(service=detail_id)
        serializer = serializers.ReviewSerializer(qs, many=True)
        return Response({"reviews": serializer.data})

    def post(self, request, entities, entity_id, detail_id):
        response = self.check_detail(entities, entity_id, detail_id)
        if response:
            return response

        key = request.headers['Authorization'][6:14]
        params = {
            'user': AuthToken.objects.get(token_key=key).user.user,
            'rating': request.data.get('rating'),
            'review': request.data.get('review')
        }
        if entities == 'clinics':
            reviews.ClinicReview.objects.create(clinic_id=detail_id, **params)
        elif entities == 'rooms':
            reviews.RoomReview.objects.create(room_id=detail_id, **params)
        elif entities == 'services':
            reviews.ServiceReview.objects.create(service_id=detail_id, **params)

        return Response(
            {"details": "Your review was saved successfully!"},
            status.HTTP_201_CREATED
        )
