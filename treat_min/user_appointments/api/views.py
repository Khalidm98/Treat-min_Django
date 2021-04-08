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
            'status__in': ["A", "R", "W"],
            'appointment_date__gte': date.today()
        }
        current_clinics = ClinicAppointment.objects.filter(**current_params)
        current_rooms = RoomAppointment.objects.filter(**current_params)
        current_services = ServiceAppointment.objects.filter(**current_params)
        current_clinics = serializers.ClinicAppointmentSerializer(current_clinics, many=True)
        current_rooms = serializers.RoomAppointmentSerializer(current_rooms, many=True)
        current_services = serializers.ServiceAppointmentSerializer(current_services, many=True)

        history_params = {
            'user': user,
            'status__in': ["A", "R"],
            'appointment_date__lt': date.today()
        }
        history_clinics = ClinicAppointment.objects.filter(**history_params)
        history_rooms = RoomAppointment.objects.filter(**history_params)
        history_services = ServiceAppointment.objects.filter(**history_params)
        history_clinics = serializers.ClinicAppointmentSerializer(history_clinics, many=True)
        history_rooms = serializers.RoomAppointmentSerializer(history_rooms, many=True)
        history_services = serializers.ServiceAppointmentSerializer(history_services, many=True)

        return Response(
            {
                "current": {
                    "clinics": current_clinics.data,
                    "rooms": current_rooms.data,
                    "services": current_services.data
                },
                "history": {
                    "clinics": history_clinics.data,
                    "rooms": history_rooms.data,
                    "services": history_services.data
                }
            }
        )


class ReserveAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    WEEK_DAYS = {"MON": 0, "TUE": 1, "WED": 2, "THU": 3, "FRI": 4, "SAT": 5, "SUN": 6}

    def post(self, request, entities, entity_id, detail_id):
        result = check_detail(entities, entity_id, detail_id)
        if isinstance(result, Response):
            return result

        serializer = serializers.ReserveSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            schedule = result.schedules.get(id=request.data.get('schedule'))
        except ClinicSchedule.DoesNotExist or RoomSchedule.DoesNotExist or ServiceSchedule.DoesNotExist:
            return Response({"details": "Wrong schedule id!"}, status.HTTP_404_NOT_FOUND)

        if self.WEEK_DAYS[schedule.day] != date.fromisoformat(request.data.get('appointment_date')).weekday():
            return Response(
                {"details": "Appointment day and schedule day are not consistent!"},
                status.HTTP_400_BAD_REQUEST
            )

        try:
            schedule.appointments.get(user=get_user(request), appointment_date=request.data.get('appointment_date'))
            return Response(
                {"details": "User cannot reserve the same schedule twice in the same day!"},
                status.HTTP_400_BAD_REQUEST
            )

        except ClinicAppointment.DoesNotExist or RoomAppointment.DoesNotExist or ServiceAppointment.DoesNotExist:
            params = {
                'user': get_user(request),
                'appointment_date': request.data.get('appointment_date'),
                'schedule_id': request.data.get('schedule')
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

    def patch(self, request, entities, entity_id, detail_id):
        # cancel an appointment (status)
        pass
