from django.urls import path
from . import views

urlpatterns = [
    path('clinics/', views.ClinicAPI.as_view()),
    path('clinics/<int:clinic_id>/details/', views.ClinicDetailAPI.as_view()),
    path('clinics/<int:clinic_id>/details/<int:detail_id>/', views.ClinicScheduleAPI.as_view()),
    path('clinics/<int:clinic_id>/details/<int:detail_id>/reviews/', views.ClinicReviewAPI.as_view()),
]
