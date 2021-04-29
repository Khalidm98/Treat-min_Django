from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from knox.auth import TokenAuthentication

from ...accounts.api.views import get_user
from ...entities_details.api.views import check_detail
from ..models import ClinicReview, RoomReview, ServiceReview
from .serializers import ReviewSerializer, RateSerializer


class ReviewAPI(APIView):
    def get(self, request, entities, entity_id, detail_id):
        result = check_detail(entities, entity_id, detail_id)
        if isinstance(result, Response):
            return result

        if entities == 'clinics':
            qs = ClinicReview.objects.filter(clinic=detail_id)
        elif entities == 'rooms':
            qs = RoomReview.objects.filter(room=detail_id)
        else:
            qs = ServiceReview.objects.filter(service=detail_id)
        serializer = ReviewSerializer(qs, many=True)
        return Response({"reviews": serializer.data})


class RateAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, entities, entity_id, detail_id):
        result = check_detail(entities, entity_id, detail_id)
        if isinstance(result, Response):
            return result

        serializer = RateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        rating = request.data.get('rating')
        user = get_user(request)

        try:
            review = result.reviews.get(user=user)
            result.rating_total = result.rating_total - int(review.rating) + int(rating)
            result.save()
            review.review = request.data.get('review')
            review.rating = rating
            review.save()
            return Response({"details": "Your review was updated successfully!"})

        except (ClinicReview.DoesNotExist, RoomReview.DoesNotExist, ServiceReview.DoesNotExist):
            result.rating_total = result.rating_total + int(rating)
            result.rating_users = result.rating_users + 1
            result.save()

            params = {
                'user': user,
                'rating': rating,
                'review': request.data.get('review')
            }
            if entities == 'clinics':
                ClinicReview.objects.create(clinic_id=detail_id, **params)
            elif entities == 'rooms':
                RoomReview.objects.create(room_id=detail_id, **params)
            elif entities == 'services':
                ServiceReview.objects.create(service_id=detail_id, **params)

            return Response(
                {"details": "Your review was saved successfully!"},
                status.HTTP_201_CREATED
            )
