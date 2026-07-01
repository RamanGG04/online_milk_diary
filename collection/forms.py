from django import forms

from collection.models import MilkEntry, RateChart


class MilkEntryForm(forms.ModelForm):
    class Meta:
        model = MilkEntry
        fields = ['farmer', 'date', 'shift', 'quantity_liters', 'fat_percent', 'snf_percent', 'notes']
        widgets = {
            'farmer': forms.Select(attrs={'class': 'form-select'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'shift': forms.Select(attrs={'class': 'form-select'}),
            'quantity_liters': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'fat_percent': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'snf_percent': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


class RateChartForm(forms.ModelForm):
    class Meta:
        model = RateChart
        fields = ['name', 'min_fat', 'max_fat', 'price_per_liter', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'min_fat': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'max_fat': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'price_per_liter': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
