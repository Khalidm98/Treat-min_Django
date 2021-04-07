from django.urls import path
from .views import DetailAPI, ScheduleAPI

urlpatterns = [
    path('<str:entities>/<int:entity_id>/details/', DetailAPI.as_view()),
    path('<str:entities>/<int:entity_id>/details/<int:detail_id>/schedules/', ScheduleAPI.as_view()),
]
