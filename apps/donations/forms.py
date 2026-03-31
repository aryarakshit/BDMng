from django import forms
from .models import Donation
from apps.donors.models import Donor
from django.core.exceptions import ValidationError
from datetime import date

class DonationForm(forms.ModelForm):
    donor_id = forms.IntegerField(widget=forms.HiddenInput(), required=True)

    class Meta:
        model = Donation
        fields = ['donation_date', 'units_collected', 'hemoglobin', 'blood_pressure', 'camp_location', 'remarks']
        widgets = {
            'donation_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'units_collected': forms.NumberInput(attrs={'class': 'form-control'}),
            'hemoglobin': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'blood_pressure': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 120/80'}),
            'camp_location': forms.TextInput(attrs={'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean_donor_id(self):
        donor_id = self.cleaned_data.get('donor_id')
        try:
            donor = Donor.objects.get(id=donor_id)
            if not donor.is_eligible:
                days_left = 90 - (date.today() - donor.last_donation).days
                raise ValidationError(f"Donor is not eligible yet. {days_left} days remaining.")
        except Donor.DoesNotExist:
            raise ValidationError("Selected donor does not exist.")
        return donor_id

    def clean(self):
        cleaned_data = super().clean()
        # Additional cross-field validation if needed
        return cleaned_data
