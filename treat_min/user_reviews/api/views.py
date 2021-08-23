from datetime import date
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from knox.auth import TokenAuthentication

from ...accounts.api.views import get_user
from ...entities_details.api.views import check_detail
from ...user_appointments.models import ClinicAppointment, ServiceAppointment
from ..models import ClinicReview, ServiceReview
from .serializers import ReviewSerializer, RateSerializer


class ReviewAPI(APIView):
    def get(self, request, entities, entity_id, detail_id):
        result = check_detail(entities, entity_id, detail_id)
        if isinstance(result, Response):
            return result

        if entities == 'clinics':
            qs = ClinicReview.objects.filter(clinic=detail_id)
        else:
            qs = ServiceReview.objects.filter(service=detail_id)
        serializer = ReviewSerializer(qs, many=True)
        return Response({"reviews": serializer.data})


class RateAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, entities, appointment_id):
        try:
            if entities == 'clinics':
                appointment = ClinicAppointment.objects.get(id=appointment_id)
                detail = appointment.schedule.clinic
            elif entities == 'services':
                appointment = ServiceAppointment.objects.get(id=appointment_id)
                detail = appointment.schedule.service
            else:
                return Response({"details": "Page not found!"}, status.HTTP_404_NOT_FOUND)

        except (ClinicAppointment.DoesNotExist, ServiceAppointment.DoesNotExist):
            return Response(
                {"details": "{0} appointment not found!".format(entities[0:len(entities) - 1])},
                status.HTTP_404_NOT_FOUND
            )

        user = get_user(request)
        if appointment.user != user:
            return Response(
                {"details": "This appointment doesn't belong to this user!"},
                status.HTTP_400_BAD_REQUEST
            )

        if appointment.appointment_date > date.today():
            return Response(
                {"details": "You cannot review a future appointment!"},
                status.HTTP_400_BAD_REQUEST
            )

        serializer = RateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        rating = request.data.get('rating')

        try:
            review = detail.reviews.get(user=user)
            detail.rating_total = detail.rating_total - int(review.rating) + int(rating)
            detail.save()
            review.review = request.data.get('review')
            review.rating = rating
            review.save()
            return Response({"details": "Your review was updated successfully."})

        except (ClinicReview.DoesNotExist, ServiceReview.DoesNotExist):
            detail.rating_total = detail.rating_total + int(rating)
            detail.rating_users = detail.rating_users + 1
            detail.save()

            params = {
                'user': user,
                'rating': rating,
                'review': request.data.get('review')
            }
            if entities == 'clinics':
                ClinicReview.objects.create(clinic_id=detail.id, **params)
            elif entities == 'services':
                ServiceReview.objects.create(service_id=detail.id, **params)

            return Response(
                {"details": "Your review was saved successfully."},
                status.HTTP_201_CREATED
            )
