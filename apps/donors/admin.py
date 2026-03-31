from django.contrib import admin
from .models import Donor


@admin.register(Donor)
class DonorAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'blood_group', 'phone', 'status', 'last_donation', 'is_eligible']
    list_filter = ['blood_group', 'status', 'gender']
    search_fields = ['full_name', 'phone', 'email']
    readonly_fields = ['created_at']
