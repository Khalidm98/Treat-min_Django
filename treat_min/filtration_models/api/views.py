from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Area,City
from .serializers import AreaSerializer,CitySerializer


class AreasAPI(APIView):
    def get(self, request):

        qs = Area.objects.all()
        serializer = AreaSerializer(qs, many=True)

        return Response(
            {
                "areas": serializer.data
            }
        )

class CitiesAPI(APIView):
    def get(self, request):

        qs = City.objects.all()
        serializer = CitySerializer(qs, many=True)

        return Response(
            {
                "cities": serializer.data
            }
        )