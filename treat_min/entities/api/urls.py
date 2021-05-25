from django.urls import path
from .views import EntityAPI, HospitalsAPI

urlpatterns = [
    path('hospitals/', HospitalsAPI.as_view()),
    path('<str:entities>/', EntityAPI.as_view()),
]
