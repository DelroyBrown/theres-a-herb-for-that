# apps\consultations\urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("consultations/", views.consultations, name="consultations"),
]

