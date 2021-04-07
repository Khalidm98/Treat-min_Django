from django.urls import path
from .views import EntityAPI

urlpatterns = [
    path('<str:entities>/', EntityAPI.as_view()),
]
