from datetime import timedelta

from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Appointment, Doctor, Specialty, TimeSlot


class AppointmentFlowTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.specialty = Specialty.objects.create(name="Généraliste")
        self.doctor = Doctor.objects.create(
            first_name="Alice",
            last_name="Martin",
            specialty=self.specialty,
            bio="Médecin généraliste expérimentée.",
            address="12 rue de la Santé",
            city="Paris",
            postal_code="75005",
            phone_number="0102030405",
            email="alice@example.com",
        )
        now = timezone.now() + timedelta(days=1)
        self.slot = TimeSlot.objects.create(
            doctor=self.doctor,
            start=now.replace(hour=10, minute=0, second=0, microsecond=0),
            end=now.replace(hour=10, minute=30, second=0, microsecond=0),
        )

    def test_home_page_lists_doctors(self):
        response = self.client.get(reverse("appointments:home"))
        self.assertContains(response, "Dr Alice Martin")

    def test_doctor_detail_and_booking(self):
        detail_url = reverse("appointments:doctor", args=[self.doctor.pk])
        response = self.client.get(detail_url)
        self.assertContains(response, "Médecin généraliste expérimentée")
        payload = {
            "patient_name": "Bob",
            "patient_email": "bob@example.com",
            "patient_phone": "0600000000",
            "reason": "Consultation annuelle",
            "slot": self.slot.pk,
        }
        response = self.client.post(detail_url, data=payload, follow=True)
        self.assertRedirects(response, reverse("appointments:confirmation", args=[Appointment.objects.get().pk]))
        self.slot.refresh_from_db()
        self.assertTrue(self.slot.is_booked)

    def test_confirmation_page_displays_summary(self):
        appointment = Appointment.objects.create(
            slot=self.slot,
            doctor=self.doctor,
            patient_name="Clara",
            patient_email="clara@example.com",
            patient_phone="0700000000",
            reason="Visite de contrôle",
        )
        self.slot.is_booked = True
        self.slot.save(update_fields=["is_booked"])

        response = self.client.get(reverse("appointments:confirmation", args=[appointment.pk]))
        self.assertContains(response, "Votre rendez-vous est confirmé")
        self.assertContains(response, "Visite de contrôle")
