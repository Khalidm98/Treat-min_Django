from django.urls import path
from .views import AreasAPI,CitiesAPI

urlpatterns = [
    path('areas', AreasAPI.as_view()),
    path('cities', CitiesAPI.as_view())
]
