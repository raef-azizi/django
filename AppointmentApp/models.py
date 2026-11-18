
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.utils import timezone


class Appointment(models.Model):

    # Les différents états d'un rendez-vous
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'En attente'
        CONFIRMED = 'CONFIRMED', 'Confirmé'
        CANCELLED = 'CANCELLED', 'Annulé'

    # Informations du rendez-vous
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

    # Relations avec Doctor et Patient
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

    # Validation de la date du rendez-vous
    def clean(self):
        super().clean()

        if not self.appointment_date:
            return

        # Récupérer l'ancienne date si le rendez-vous existe déjà
        if self.pk:
            old_date = type(self).objects.filter(
                pk=self.pk
            ).values_list(
                'appointment_date',
                flat=True
            ).first()

            # Autoriser la modification d'un ancien rendez-vous
            # si sa date n'a pas été changée
            if old_date == self.appointment_date:
                return

        # Refuser une date passée ou égale à maintenant
        if self.appointment_date <= timezone.now():
            raise ValidationError({
                'appointment_date':
                    "La date du rendez-vous doit être dans le futur."
            })

    class Meta:
        ordering = ['appointment_date']

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
