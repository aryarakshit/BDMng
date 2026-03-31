from django.db import models
from django.conf import settings

class BloodRequest(models.Model):
    PRIORITY_CHOICES = [('normal', 'Normal'), ('urgent', 'Urgent'), ('emergency', 'Emergency')]
    STATUS_CHOICES   = [('pending', 'Pending'), ('approved', 'Approved'),
                        ('rejected', 'Rejected'), ('fulfilled', 'Fulfilled')]

    patient_name     = models.CharField(max_length=200)
    hospital         = models.CharField(max_length=200)
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ]

    blood_group      = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES)
    units_required   = models.PositiveIntegerField()
    priority         = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='normal')
    status           = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    doctor_notes     = models.TextField(blank=True)
    requested_by     = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    allocated_units  = models.ManyToManyField('inventory.BloodUnit', blank=True)
    created_at       = models.DateTimeField(auto_now_add=True)
    resolved_at      = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Request for {self.patient_name} ({self.blood_group})"
