from django import forms
from .models import BloodUnit

class BloodUnitForm(forms.ModelForm):
    collection_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    expiry_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = BloodUnit
        fields = ['blood_group', 'units', 'collection_date', 'expiry_date', 'source_donor', 'status']

    def clean(self):
        cleaned_data = super().clean()
        collection_date = cleaned_data.get('collection_date')
        expiry_date = cleaned_data.get('expiry_date')
        if collection_date and expiry_date and expiry_date <= collection_date:
            raise forms.ValidationError("Expiry date must be after collection date.")
        return cleaned_data
