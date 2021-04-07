from django.urls import path
from .views import AppointmentAPI, ReserveAPI

urlpatterns = [
    path('user/appointments/', AppointmentAPI.as_view()),
    path('<str:entities>/<int:entity_id>/details/<int:detail_id>/reserve/', ReserveAPI.as_view()),
]
