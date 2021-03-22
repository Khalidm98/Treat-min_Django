from django.urls import path
from . import views

urlpatterns = [
    path('clinics/', views.ClinicList.as_view()),
    path('clinics/<int:clinic_id>/details/', views.ClinicDetailList.as_view()),
    path('clinics/<int:clinic_id>/details/<int:detail_id>/', views.ClinicDetailSchedules.as_view()),
    path('clinics/<int:clinic_id>/details/<int:detail_id>/reviews/', views.ClinicReviewsList.as_view()),
]
