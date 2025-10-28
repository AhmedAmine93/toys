from django import forms

from .models import Appointment, TimeSlot


class AppointmentForm(forms.ModelForm):
    slot = forms.ModelChoiceField(
        queryset=TimeSlot.objects.none(),
        widget=forms.RadioSelect,
        empty_label=None,
        label="Choisissez un créneau"
    )

    class Meta:
        model = Appointment
        fields = [
            "patient_name",
            "patient_email",
            "patient_phone",
            "reason",
            "slot",
        ]
        labels = {
            "patient_name": "Votre nom",
            "patient_email": "Adresse e-mail",
            "patient_phone": "Téléphone",
            "reason": "Motif de consultation",
        }

    def __init__(self, *args, **kwargs):
        available_slots = kwargs.pop("available_slots", TimeSlot.objects.none())
        super().__init__(*args, **kwargs)
        self.fields["slot"].queryset = available_slots

    def save(self, commit=True):
        appointment = super().save(commit=False)
        appointment.doctor = appointment.slot.doctor
        if commit:
            appointment.save()
            appointment.slot.is_booked = True
            appointment.slot.save(update_fields=["is_booked"])
        return appointment
