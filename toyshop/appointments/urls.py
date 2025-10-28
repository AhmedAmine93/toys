from django.urls import path

from . import views

app_name = "appointments"

urlpatterns = [
    path("", views.home, name="home"),
    path("specialites/<int:specialty_id>/", views.specialty_detail, name="specialty"),
    path("medecins/<int:doctor_id>/", views.doctor_detail, name="doctor"),
    path("confirmation/<int:appointment_id>/", views.appointment_confirmation, name="confirmation"),
]
