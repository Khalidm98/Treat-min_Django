from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import AreaSerializer, CitySerializer
from ..models import Area, City


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
