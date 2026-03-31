from django.db import models
from datetime import date
from django.conf import settings

class Donor(models.Model):
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ]
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')]
    STATUS_CHOICES = [('active', 'Active'), ('inactive', 'Inactive'), ('deferred', 'Deferred')]

    full_name        = models.CharField(max_length=200)
    date_of_birth    = models.DateField()
    gender           = models.CharField(max_length=1, choices=GENDER_CHOICES)
    blood_group      = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES)
    phone            = models.CharField(max_length=15, unique=True)
    email            = models.EmailField(blank=True)
    address          = models.TextField(blank=True)
    medical_history  = models.TextField(blank=True)
    status           = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    created_at       = models.DateTimeField(auto_now_add=True)
    last_donation    = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.full_name} ({self.blood_group})"

    @property
    def is_eligible(self):
        if not self.last_donation:
            return True
        return (date.today() - self.last_donation).days >= 90
