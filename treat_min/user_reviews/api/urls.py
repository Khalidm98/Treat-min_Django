from django.urls import path
from .views import ReviewAPI, RateAPI

urlpatterns = [
    path('<str:entities>/<int:entity_id>/details/<int:detail_id>/reviews/', ReviewAPI.as_view()),
    path('user/appointments/<str:entities>/<int:appointment_id>/review/', RateAPI.as_view()),
]
