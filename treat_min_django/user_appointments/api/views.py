from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import ClinicAppointmentSerializer , ClinicAppointmentStatusSerializer
from rest_framework import generics, status
from ..models import ClinicAppointment
from django.http import Http404




class MakeClinicAppointmentView(generics.GenericAPIView):

    serializer_class = ClinicAppointmentSerializer

    def post(self, request, *args, **kwargs):
        token = "cwekjcbwhbe1f23" #needs to be modified
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if(token == "cwekjcbwhbe1f23"): #needs to be modified as well
            serializer.save()
            return Response({
                "details": "Your Appointment request has been sent successfully, please wait for admin acceptance."
            },
                status=status.HTTP_201_CREATED
            )
        else:
            return Response({
                "details": "Couldn't identify user , please login and try again."
            },
                status=status.HTTP_404_NOT_FOUND
            )


class ClinicAppointmentStatusView(generics.GenericAPIView):

    serializer_class = ClinicAppointmentStatusSerializer

    def get(self, request):
        appointments = ClinicAppointment.objects.filter(status__exact='W')
        serializer = ClinicAppointmentStatusSerializer(appointments, many=True)
        if appointments.exists():
            return Response({"Pending Appointment Requests": serializer.data},
                            status=status.HTTP_200_OK)
        else:
            return Response({"details": "No records found"},
                            status=status.HTTP_404_NOT_FOUND)


class ClinicAppointmentStatusChangeView(generics.GenericAPIView):

    serializer_class = ClinicAppointmentStatusSerializer

    def get(self, request, appointment_id):
        appointment = ClinicAppointment.objects.get(id=appointment_id)
        try:
            appointment
        except appointment.DoesNotExist:
            raise Http404

        serializer = ClinicAppointmentStatusSerializer(appointment)

        return Response(serializer.data, status=status.HTTP_200_OK)





    def patch(self, request, appointment_id):
        appointment = ClinicAppointment.objects.get(id=appointment_id)
        serializer = ClinicAppointmentStatusSerializer(appointment, data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_200_OK)
        return Response({"details": "Wrong Parameters"},
                            status=status.HTTP_400_BAD_REQUEST)




