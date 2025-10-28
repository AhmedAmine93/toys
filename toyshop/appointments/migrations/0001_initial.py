# Generated manually to define initial schema for appointments app
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Specialty",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120, unique=True)),
                ("description", models.TextField(blank=True)),
            ],
            options={"ordering": ["name"]},
        ),
        migrations.CreateModel(
            name="Doctor",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("first_name", models.CharField(max_length=80)),
                ("last_name", models.CharField(max_length=80)),
                ("bio", models.TextField(blank=True)),
                ("address", models.CharField(max_length=255)),
                ("city", models.CharField(max_length=120)),
                ("postal_code", models.CharField(max_length=20)),
                ("phone_number", models.CharField(max_length=30)),
                ("email", models.EmailField(max_length=254)),
                (
                    "specialty",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="doctors",
                        to="appointments.specialty",
                    ),
                ),
            ],
            options={"ordering": ["last_name", "first_name"], "unique_together": {("first_name", "last_name", "specialty", "city")}},
        ),
        migrations.CreateModel(
            name="TimeSlot",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("start", models.DateTimeField()),
                ("end", models.DateTimeField()),
                ("is_booked", models.BooleanField(default=False)),
                (
                    "doctor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="time_slots",
                        to="appointments.doctor",
                    ),
                ),
            ],
            options={"ordering": ["start"], "unique_together": {("doctor", "start")}},
        ),
        migrations.CreateModel(
            name="Appointment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "status",
                    models.CharField(
                        choices=[("scheduled", "Scheduled"), ("cancelled", "Cancelled")],
                        default="scheduled",
                        max_length=20,
                    ),
                ),
                ("patient_name", models.CharField(max_length=120)),
                ("patient_email", models.EmailField(max_length=254)),
                ("patient_phone", models.CharField(max_length=30)),
                ("reason", models.CharField(max_length=255)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "doctor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="appointments",
                        to="appointments.doctor",
                    ),
                ),
                (
                    "slot",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="appointment",
                        to="appointments.timeslot",
                    ),
                ),
            ],
            options={"ordering": ["-created_at"]},
        ),
    ]
