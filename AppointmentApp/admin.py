
from django.contrib import admin
from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'doctor',
        'patient',
        'appointment_date',
        'status',
        'duration_minutes',
    )

    list_filter = ('status', 'appointment_date')

    search_fields = (
        'doctor__username',
        'patient__username',
        'reason',
    )
