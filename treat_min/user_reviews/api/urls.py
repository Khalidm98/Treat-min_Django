from django.urls import path
from .views import ReviewAPI, RateAPI

urlpatterns = [
    path('<str:entities>/<int:entity_id>/details/<int:detail_id>/reviews/', ReviewAPI.as_view()),
    path('<str:entities>/<int:entity_id>/details/<int:detail_id>/rate/', RateAPI.as_view()),
    # change this url
]
