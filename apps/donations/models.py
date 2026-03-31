from django.db import models
from datetime import date
from django.conf import settings

class Donation(models.Model):
    donor            = models.ForeignKey('donors.Donor', on_delete=models.CASCADE, related_name='donations')
    donation_date    = models.DateField(default=date.today)
    units_collected  = models.PositiveIntegerField(default=1)
    hemoglobin       = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    blood_pressure   = models.CharField(max_length=10, blank=True)  # e.g. "120/80"
    camp_location    = models.CharField(max_length=200, blank=True)
    collected_by     = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    remarks          = models.TextField(blank=True)
    blood_unit       = models.OneToOneField('inventory.BloodUnit', null=True, blank=True,
                                             on_delete=models.SET_NULL, related_name='donation')
    created_at       = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-donation_date']

    def __str__(self):
        return f"Donation by {self.donor.full_name} on {self.donation_date}"
