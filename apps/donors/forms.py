from django import forms
from .models import Donor
from datetime import date

class DonorForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Donor
        exclude = ['created_at', 'last_donation']
        widgets = {
            'medical_history': forms.Textarea(attrs={'rows': 3}),
            'address': forms.Textarea(attrs={'rows': 2}),
        }

    def clean_date_of_birth(self):
        dob = self.cleaned_data['date_of_birth']
        age = (date.today() - dob).days // 365
        if age < 18 or age > 65:
            raise forms.ValidationError("Donor must be between 18 and 65 years old.")
        return dob
