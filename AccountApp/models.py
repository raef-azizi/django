
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator, RegexValidator
from django.core.exceptions import ValidationError
from django.utils import timezone


# User model
class User(AbstractUser):
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"


# Specialty model
class Specialty(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Specialty"
        verbose_name_plural = "Specialties"

    def __str__(self):
        return self.name


# Doctor model
class Doctor(User):
    license_number = models.CharField(
        max_length=6,
        unique=True,
        validators=[MinLengthValidator(6)]
    )

    phone = models.CharField(
        max_length=8,
        validators=[
            RegexValidator(
                regex=r'^\d{8}$',
                message="Le téléphone doit contenir exactement 8 chiffres."
            )
        ]
    )

    specialties = models.ManyToManyField(
        Specialty,
        related_name='doctors'
    )

    class Meta:
        verbose_name = "Doctor"
        verbose_name_plural = "Doctors"

    def __str__(self):
        return f"Dr. {self.first_name} {self.last_name}"


# Birth date validation
def validate_birth_date(value):
    if value >= timezone.localdate():
        raise ValidationError(
            "La date de naissance doit être antérieure à aujourd'hui."
        )


# Patient model
class Patient(User):
    national_id = models.CharField(
        max_length=8,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\d{8}$',
                message="Le numéro national doit contenir exactement 8 chiffres."
            )
        ]
    )

    phone = models.CharField(
        max_length=8,
        validators=[
            RegexValidator(
                regex=r'^\d{8}$',
                message="Le téléphone doit contenir exactement 8 chiffres."
            )
        ]
    )

    birth_date = models.DateField(
        validators=[validate_birth_date]
    )

    class Meta:
        verbose_name = "Patient"
        verbose_name_plural = "Patients"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
