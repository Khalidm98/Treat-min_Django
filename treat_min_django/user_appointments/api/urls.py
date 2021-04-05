from django.urls import path
from .views import MakeClinicAppointmentView , ClinicAppointmentStatusView ,ClinicAppointmentStatusChangeView

urlpatterns = [
    path('make_appointment/', MakeClinicAppointmentView.as_view()),
    path('change_status/',  ClinicAppointmentStatusView.as_view(),),
    path('change_status/<int:appointment_id>/',  ClinicAppointmentStatusChangeView.as_view()),
    ]
