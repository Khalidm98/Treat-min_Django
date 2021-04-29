from datetime import date

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from knox.auth import TokenAuthentication

from ...accounts.api.views import get_user
from ...entities_details.api.views import check_detail
from ...entities_details.models import ClinicSchedule, RoomSchedule, ServiceSchedule
from ..models import ClinicAppointment, RoomAppointment, ServiceAppointment
from . import serializers


class AppointmentAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = get_user(request)
        current_params = {
            'user': user,
            'status__in': ['A', 'R', 'W'],
            'appointment_date__gte': date.today()
        }
        current_clinics = ClinicAppointment.objects.filter(**current_params)
        current_rooms = RoomAppointment.objects.filter(**current_params)
        current_services = ServiceAppointment.objects.filter(**current_params)
        current_clinics = serializers.ClinicAppointmentSerializer(current_clinics, many=True)
        current_rooms = serializers.RoomAppointmentSerializer(current_rooms, many=True)
        current_services = serializers.ServiceAppointmentSerializer(current_services, many=True)

        past_params = {
            'user': user,
            'status__in': ["A", "R"],
            'appointment_date__lt': date.today()
        }
        past_clinics = ClinicAppointment.objects.filter(**past_params)
        past_rooms = RoomAppointment.objects.filter(**past_params)
        past_services = ServiceAppointment.objects.filter(**past_params)
        past_clinics = serializers.ClinicAppointmentSerializer(past_clinics, many=True)
        past_rooms = serializers.RoomAppointmentSerializer(past_rooms, many=True)
        past_services = serializers.ServiceAppointmentSerializer(past_services, many=True)

        return Response(
            {
                "current": {
                    "clinics": current_clinics.data,
                    "rooms": current_rooms.data,
                    "services": current_services.data
                },
                "past": {
                    "clinics": past_clinics.data,
                    "rooms": past_rooms.data,
                    "services": past_services.data
                }
            }
        )


class CancelAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, entities, appointment_id):
        try:
            if entities == 'clinics':
                appointment = ClinicAppointment.objects.get(id=appointment_id)
            elif entities == 'rooms':
                appointment = RoomAppointment.objects.get(id=appointment_id)
            elif entities == 'services':
                appointment = ServiceAppointment.objects.get(id=appointment_id)
            else:
                return Response({"details": "Page not found!"}, status.HTTP_404_NOT_FOUND)

        except (ClinicAppointment.DoesNotExist, RoomAppointment.DoesNotExist, ServiceAppointment.DoesNotExist):
            return Response(
                {"details": "{0} appointment not found!".format(entities[0:len(entities) - 1])},
                status.HTTP_404_NOT_FOUND
            )

        user = get_user(request)
        if appointment.user != user:
            return Response(
                {"details": "This appointment doesn't belong to this user"},
                status.HTTP_400_BAD_REQUEST
            )

        if appointment.appointment_date < date.today():
            return Response(
                {"details": "You cannot cancel a past appointment"},
                status.HTTP_400_BAD_REQUEST
            )

        appointment.status = 'C'
        appointment.save()
        return Response({"details": "Your appointment was canceled successfully!"})


class ReserveAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    WEEK_DAYS = {"MON": 0, "TUE": 1, "WED": 2, "THU": 3, "FRI": 4, "SAT": 5, "SUN": 6}

    def post(self, request, entities, entity_id, detail_id):
        result = check_detail(entities, entity_id, detail_id)
        if isinstance(result, Response):
            return result

        if entities == 'clinics':
            serializer = serializers.ClinicReserveSerializer(data=request.data)
        elif entities == 'rooms':
            serializer = serializers.RoomReserveSerializer(data=request.data)
        else:
            serializer = serializers.ServiceReserveSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        user = get_user(request)
        schedule_id = request.data.get('schedule')
        appointment_date = request.data.get('appointment_date')

        try:
            schedule = result.schedules.get(id=schedule_id)
        except (ClinicSchedule.DoesNotExist, RoomSchedule.DoesNotExist, ServiceSchedule.DoesNotExist):
            return Response({"details": "Wrong schedule id!"}, status.HTTP_404_NOT_FOUND)

        if date.fromisoformat(appointment_date) <= date.today():
            return Response(
                {"details": "Appointment day must be after today!"},
                status.HTTP_400_BAD_REQUEST
            )

        if self.WEEK_DAYS[schedule.day] != date.fromisoformat(appointment_date).weekday():
            return Response(
                {"details": "Appointment day and schedule day are not consistent!"},
                status.HTTP_400_BAD_REQUEST
            )

        try:
            schedule.appointments.get(user=user, appointment_date=appointment_date)
            return Response(
                {"details": "User cannot reserve the same schedule twice in the same day!"},
                status.HTTP_400_BAD_REQUEST
            )

        except (ClinicAppointment.DoesNotExist, RoomAppointment.DoesNotExist, ServiceAppointment.DoesNotExist):
            params = {
                'user': user,
                'schedule_id': schedule_id,
                'appointment_date': appointment_date
            }
            if entities == 'clinics':
                ClinicAppointment.objects.create(**params)
            elif entities == 'rooms':
                RoomAppointment.objects.create(**params)
            elif entities == 'services':
                ServiceAppointment.objects.create(**params)

            return Response(
                {"details": "Your appointment was reserved successfully!"},
                status.HTTP_201_CREATED
            )
