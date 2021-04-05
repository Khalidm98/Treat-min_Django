from django.urls import path
from . import views

urlpatterns = [
    path('<str:entities>/', views.EntityAPI.as_view()),
    path('<str:entities>/<int:entity_id>/details/', views.DetailAPI.as_view()),
    path('<str:entities>/<int:entity_id>/details/<int:detail_id>/schedules/', views.ScheduleAPI.as_view()),
    path('<str:entities>/<int:entity_id>/details/<int:detail_id>/appointments/', views.AppointmentAPI.as_view()),
    path('<str:entities>/<int:entity_id>/details/<int:detail_id>/reviews/', views.ReviewAPI.as_view()),
]
