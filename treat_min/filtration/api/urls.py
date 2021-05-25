from django.urls import path
from .views import AreasAPI, CitiesAPI, CitiesAreasAPI

urlpatterns = [
    path('areas/', AreasAPI.as_view()),
    path('cities/', CitiesAPI.as_view()),
    path('cities/<str:city_id>/areas/', CitiesAreasAPI.as_view()),
]
