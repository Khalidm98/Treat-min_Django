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
