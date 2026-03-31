from django.contrib import admin
from .models import Donation


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ['donor', 'donation_date', 'units_collected', 'blood_unit', 'camp_location']
    list_filter = ['donation_date', 'donor__blood_group']
    search_fields = ['donor__full_name', 'donor__phone']
    readonly_fields = ['created_at']
