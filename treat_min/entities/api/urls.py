from django.urls import path
from .views import EntityAPI,HospitalsAPI

urlpatterns = [
    path('<str:entities>/', EntityAPI.as_view()),
    path('hospitals', HospitalsAPI.as_view()),

]
