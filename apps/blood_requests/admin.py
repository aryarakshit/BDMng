from django.contrib import admin
from .models import BloodRequest


@admin.register(BloodRequest)
class BloodRequestAdmin(admin.ModelAdmin):
    list_display = ['patient_name', 'hospital', 'blood_group', 'units_required', 'priority', 'status', 'created_at']
    list_filter = ['blood_group', 'priority', 'status']
    search_fields = ['patient_name', 'hospital']
    readonly_fields = ['created_at', 'resolved_at']
