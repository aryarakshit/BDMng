from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Donation

@receiver(post_save, sender=Donation)
def update_donor_last_donation(sender, instance, created, **kwargs):
    if created:
        donor = instance.donor
        donor.last_donation = instance.donation_date
        donor.save(update_fields=['last_donation'])
