from django import forms

from billing.models import Deduction, Payment


class DeductionForm(forms.ModelForm):
    class Meta:
        model = Deduction
        fields = ['farmer', 'deduction_type', 'amount', 'month', 'description']
        widgets = {
            'farmer': forms.Select(attrs={'class': 'form-select'}),
            'deduction_type': forms.Select(attrs={'class': 'form-select'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'month': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
        }


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['paid_amount', 'payment_mode', 'paid_on', 'status']
        widgets = {
            'paid_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'payment_mode': forms.Select(attrs={'class': 'form-select'}),
            'paid_on': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
