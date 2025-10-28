from django.db import models
from django.utils import timezone


class Specialty(models.Model):
    name = models.CharField(max_length=120, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Doctor(models.Model):
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    specialty = models.ForeignKey(Specialty, related_name="doctors", on_delete=models.PROTECT)
    bio = models.TextField(blank=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=120)
    postal_code = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=30)
    email = models.EmailField()

    class Meta:
        ordering = ["last_name", "first_name"]
        unique_together = (("first_name", "last_name", "specialty", "city"),)

    def __str__(self) -> str:
        return f"Dr {self.first_name} {self.last_name}"

    @property
    def full_address(self) -> str:
        return f"{self.address}, {self.postal_code} {self.city}"


class TimeSlotQuerySet(models.QuerySet):
    def upcoming(self):
        return self.filter(start__gte=timezone.now()).order_by("start")

    def available(self):
        return self.filter(is_booked=False, start__gte=timezone.now()).order_by("start")


class TimeSlot(models.Model):
    doctor = models.ForeignKey(Doctor, related_name="time_slots", on_delete=models.CASCADE)
    start = models.DateTimeField()
    end = models.DateTimeField()
    is_booked = models.BooleanField(default=False)

    objects = TimeSlotQuerySet.as_manager()

    class Meta:
        ordering = ["start"]
        unique_together = (("doctor", "start"),)

    def __str__(self) -> str:
        return f"{self.doctor} - {self.start:%d/%m/%Y %H:%M}"

    def duration_minutes(self) -> int:
        return int((self.end - self.start).total_seconds() // 60)


class Appointment(models.Model):
    STATUS_SCHEDULED = "scheduled"
    STATUS_CANCELLED = "cancelled"
    STATUS_CHOICES = (
        (STATUS_SCHEDULED, "Scheduled"),
        (STATUS_CANCELLED, "Cancelled"),
    )

    slot = models.OneToOneField(TimeSlot, related_name="appointment", on_delete=models.PROTECT)
    doctor = models.ForeignKey(Doctor, related_name="appointments", on_delete=models.CASCADE)
    patient_name = models.CharField(max_length=120)
    patient_email = models.EmailField()
    patient_phone = models.CharField(max_length=30)
    reason = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_SCHEDULED)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Appointment with {self.doctor} for {self.patient_name}"
