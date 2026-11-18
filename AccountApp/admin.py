
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Doctor, Patient, Specialty


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    pass


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'license_number', 'phone')
    search_fields = ('username', 'first_name', 'last_name', 'license_number')

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('license_number',)
        return ()


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'national_id', 'phone')
    search_fields = ('username', 'first_name', 'last_name', 'national_id')

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('national_id',)
        return ()


@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
