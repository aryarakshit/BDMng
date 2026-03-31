from django.db import models
from datetime import date
from django.conf import settings

class BloodUnit(models.Model):
    STATUS_CHOICES = [('available', 'Available'), ('reserved', 'Reserved'),
                      ('used', 'Used'), ('expired', 'Expired'), ('discarded', 'Discarded')]

    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ]

    blood_group      = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES)
    units            = models.PositiveIntegerField()
    collection_date  = models.DateField()
    expiry_date      = models.DateField()
    source_donor     = models.ForeignKey('donors.Donor', null=True, blank=True,
                                          on_delete=models.SET_NULL, related_name='units')
    status           = models.CharField(max_length=10, choices=STATUS_CHOICES, default='available')
    added_by         = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at       = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['expiry_date']

    @property
    def is_expired(self):
        return date.today() >= self.expiry_date

    @property
    def days_to_expiry(self):
        return (self.expiry_date - date.today()).days

    def __str__(self):
        return f"{self.blood_group} - {self.units} units (Exp: {self.expiry_date})"
