from django.urls import path
from treat_min_django.treat_min.api import views

urlpatterns = [
    path('clinics/', views.ClinicList.as_view()),
    path('clinics/<int:clinic_id>/schedules/', views.ClinicScheduleList.as_view()),
    path('clinics/<int:clinic_id>/schedules/<int:schedule_id>/', views.ClinicBooking.as_view()),
]
