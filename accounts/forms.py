from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import User
from farmers.models import Farmer


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
    )


class UserRegisterForm(UserCreationForm):
    role = forms.ChoiceField(choices=User.Role.choices, widget=forms.Select(attrs={'class': 'form-select'}))
    phone = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone', 'role', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'


class PublicUserRegisterForm(UserCreationForm):
    phone = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone (optional)'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'
        # Remove role field if it exists
        if 'role' in self.fields:
            del self.fields['role']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.Role.FARMER
        if commit:
            user.save()
            Farmer.objects.create(
                user=user,
                farmer_id=f'F{user.id:04}',
                name=f'{user.first_name} {user.last_name}'.strip() or user.username,
                phone=user.phone or '',
                village='',
            )
        return user
