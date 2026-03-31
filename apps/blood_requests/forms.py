from django import forms
from .models import BloodRequest

class BloodRequestForm(forms.ModelForm):
    class Meta:
        model = BloodRequest
        fields = ['patient_name', 'hospital', 'blood_group', 'units_required', 'priority', 'doctor_notes']
        widgets = {
            'patient_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Full Name'}),
            'hospital': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Hospital Name'}),
            'blood_group': forms.Select(choices=[
                ('', 'Select Group'),
                ('A+', 'A+'), ('A-', 'A-'),
                ('B+', 'B+'), ('B-', 'B-'),
                ('AB+', 'AB+'), ('AB-', 'AB-'),
                ('O+', 'O+'), ('O-', 'O-')
            ], attrs={'class': 'form-select'}),
            'units_required': forms.NumberInput(attrs={'class': 'form-input', 'min': 1}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'doctor_notes': forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'Additional notes...'}),
        }

    def clean_units_required(self):
        units = self.cleaned_data.get('units_required')
        if units <= 0:
            raise forms.ValidationError("Units required must be at least 1.")
        return units
