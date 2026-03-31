from django.contrib import admin
from .models import BloodUnit


@admin.register(BloodUnit)
class BloodUnitAdmin(admin.ModelAdmin):
    list_display = ['blood_group', 'units', 'status', 'collection_date', 'expiry_date', 'source_donor']
    list_filter = ['blood_group', 'status']
    search_fields = ['source_donor__full_name']
    readonly_fields = ['created_at']
