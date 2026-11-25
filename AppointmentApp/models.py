
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.utils import timezone


class Appointment(models.Model):

    # Different appointment statuses
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'En attente'
        CONFIRMED = 'CONFIRMED', 'Confirmé'
        CANCELLED = 'CANCELLED', 'Annulé'

    # Appointment information
    appointment_date = models.DateTimeField()

    reason = models.TextField()

    prescription = models.FileField(
        upload_to='prescriptions/',
        blank=True,
        validators=[
            FileExtensionValidator(allowed_extensions=['pdf'])
        ]
    )

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING
    )

    duration_minutes = models.PositiveIntegerField(default=30)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    # Relations with Doctor and Patient
    doctor = models.ForeignKey(
        'AccountApp.Doctor',
        on_delete=models.CASCADE,
        related_name='appointments'
    )

    patient = models.ForeignKey(
        'AccountApp.Patient',
        on_delete=models.CASCADE,
        related_name='appointments'
    )

    # Appointment date validation
    def clean(self):
        super().clean()

        if not self.appointment_date:
            return

        # Retrieve the old date if the appointment already exists
        if self.pk:
            old_date = type(self).objects.filter(
                pk=self.pk
            ).values_list(
                'appointment_date',
                flat=True
            ).first()

            # Allow modification if the date hasn't changed
            if old_date == self.appointment_date:
                return

        # Reject past or current appointment dates
        if self.appointment_date <= timezone.now():
            raise ValidationError({
                'appointment_date':
                    "La date du rendez-vous doit être dans le futur."
            })

    class Meta:
        ordering = ['appointment_date']

        verbose_name = "Appointment"
        verbose_name_plural = "Appointments"

        constraints = [
            models.UniqueConstraint(
                fields=['doctor', 'appointment_date'],
                name='unique_doctor_appointment_datetime'
            )
        ]

    def __str__(self):
        return (
            f"Rendez-vous de {self.patient} "
            f"avec {self.doctor} "
            f"le {self.appointment_date}"
        )
