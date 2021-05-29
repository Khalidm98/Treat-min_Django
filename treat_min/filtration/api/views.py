from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import AreaSerializer, CitySerializer
from ..models import Area, City
from ...entities.models import Hospital
from ...entities.api.serializers import HospitalNameSerializer

class AreasAPI(APIView):
    def get(self, request):
        qs = Area.objects.all()
        serializer = AreaSerializer(qs, many=True)
        return Response({"areas": serializer.data})


class CitiesAPI(APIView):
    def get(self, request):
        qs = City.objects.all()
        serializer = CitySerializer(qs, many=True)
        return Response({"cities": serializer.data})


class CitiesAreasAPI(APIView):
    def get(self, request, city_id):
        try:
            City.objects.get(id=city_id)
        except City.DoesNotExist:
            return Response(
                {"details": "City not found!"},
                status.HTTP_404_NOT_FOUND
            )

        qs = Area.objects.filter(city_id=city_id)
        serializer = AreaSerializer(qs, many=True)
        return Response({"areas": serializer.data})


class CityAreaHospitalsAPI(APIView):
    def get(self, request, city_id, area_id):
        try:
            City.objects.get(id=city_id)
        except City.DoesNotExist:
            return Response(
                {"details": "No city is found for the given id!"},
                status.HTTP_404_NOT_FOUND
            )
        try:
            Area.objects.get(id=area_id, city__id= city_id)
        except Area.DoesNotExist:
            return Response(
                {"details": "No area is found for the given id!"},
                status.HTTP_404_NOT_FOUND
            )

        qs = Hospital.objects.filter(city__id=city_id, area__id=area_id)
        serializer = HospitalNameSerializer(qs, many=True)
        return Response({"hospitals": serializer.data})