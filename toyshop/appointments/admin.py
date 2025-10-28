from django.contrib import admin

from .models import Appointment, Doctor, Specialty, TimeSlot


@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


class TimeSlotInline(admin.TabularInline):
    model = TimeSlot
    extra = 1
    fields = ("start", "end", "is_booked")
    ordering = ("start",)


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "specialty", "city")
    list_filter = ("specialty", "city")
    search_fields = ("first_name", "last_name", "specialty__name")
    inlines = [TimeSlotInline]


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("doctor", "patient_name", "slot", "status", "created_at")
    list_filter = ("status", "doctor__specialty")
    search_fields = ("patient_name", "doctor__last_name", "doctor__specialty__name")
    autocomplete_fields = ("doctor", "slot")
    date_hierarchy = "slot__start"
