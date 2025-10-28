from django.contrib import messages
from django.db.models import Count, Prefetch
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import AppointmentForm
from .models import Appointment, Doctor, Specialty, TimeSlot


def home(request):
    specialties = Specialty.objects.annotate(doctor_count=Count("doctors"))
    doctors = (
        Doctor.objects.select_related("specialty")
        .prefetch_related(
            Prefetch("time_slots", queryset=TimeSlot.objects.available()[:3], to_attr="next_slots")
        )
        .all()
    )
    return render(
        request,
        "appointments/home.html",
        {
            "specialties": specialties,
            "doctors": doctors,
        },
    )


def specialty_detail(request, specialty_id):
    specialty = get_object_or_404(Specialty, pk=specialty_id)
    doctors = (
        Doctor.objects.select_related("specialty")
        .filter(specialty=specialty)
        .prefetch_related(
            Prefetch("time_slots", queryset=TimeSlot.objects.available()[:3], to_attr="next_slots")
        )
    )
    return render(
        request,
        "appointments/specialty_detail.html",
        {
            "specialty": specialty,
            "doctors": doctors,
        },
    )


def doctor_detail(request, doctor_id):
    doctor = get_object_or_404(Doctor.objects.select_related("specialty"), pk=doctor_id)
    available_slots = doctor.time_slots.available()
    form = AppointmentForm(request.POST or None, available_slots=available_slots)

    if request.method == "POST" and form.is_valid():
        appointment = form.save()
        messages.success(
            request,
            "Votre rendez-vous a été réservé avec succès ! Vous recevrez un e-mail de confirmation.",
        )
        return redirect(reverse("appointments:confirmation", args=[appointment.pk]))

    return render(
        request,
        "appointments/doctor_detail.html",
        {
            "doctor": doctor,
            "available_slots": available_slots,
            "form": form,
        },
    )


def appointment_confirmation(request, appointment_id):
    appointment = get_object_or_404(
        Appointment.objects.select_related("doctor", "doctor__specialty", "slot"),
        pk=appointment_id,
    )
    return render(
        request,
        "appointments/appointment_confirmation.html",
        {
            "appointment": appointment,
        },
    )
