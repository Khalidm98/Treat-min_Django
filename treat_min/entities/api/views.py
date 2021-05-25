from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from ..models import Clinic, Service, Hospital
from .serializers import EntitySerializer, HospitalNameSerializer


def check_entity(entities, entity_id):
    try:
        if entities == 'clinics':
            entity = Clinic.objects.get(id=entity_id)
        elif entities == 'services':
            entity = Service.objects.get(id=entity_id)
        else:
            return Response({"details": "Page not found!"}, status.HTTP_404_NOT_FOUND)
        return entity

    except (Clinic.DoesNotExist, Service.DoesNotExist):
        return Response(
            {"details": "{0} not found!".format(entities[0:len(entities) - 1])},
            status.HTTP_404_NOT_FOUND
        )


class EntityAPI(APIView):
    def get(self, request, entities):
        if entities == 'clinics':
            qs = Clinic.objects.all()
        elif entities == 'services':
            qs = Service.objects.all()
        else:
            return Response({"details": "Page not found!"}, status.HTTP_404_NOT_FOUND)
        serializer = EntitySerializer(qs, many=True)
        return Response({entities: serializer.data})


class HospitalsAPI(APIView):
    def get(self, request):
        qs = Hospital.objects.all()
        serializer = HospitalNameSerializer(qs, many=True)
        return Response({"hospitals": serializer.data})
