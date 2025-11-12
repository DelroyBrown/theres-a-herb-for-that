# apps\consultations\urls.py
from django.urls import path
from . import views

app_name = "consultations"

urlpatterns = [
    path("consultations/", views.consultations, name="consultations"),
    path(
        "consultations/sent/<int:pk>/",
        views.consultation_sent,
        name="consultation_sent",
    ),
]
