from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from accounts.decorators import role_required
from accounts.forms import LoginForm, PublicUserRegisterForm, UserRegisterForm


def login_view(request):
    if request.user.is_authenticated:
        return redirect('reports:dashboard')

    role = request.GET.get('role', '')
    form = LoginForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        return redirect('reports:dashboard')

    return render(request, 'accounts/login.html', {'form': form, 'role': role})


def auth_view(request):
    if request.user.is_authenticated:
        return redirect('reports:dashboard')

    form = LoginForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        return redirect('reports:dashboard')

    return render(request, 'accounts/auth.html', {'form': form})


def farmer_register_view(request):
    if request.user.is_authenticated:
        return redirect('reports:dashboard')

    form = PublicUserRegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, 'Your account has been created and you are now logged in.')
        return redirect('reports:dashboard')

    return render(request, 'accounts/farmer_register.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('accounts:login')


def home_view(request):
    if request.user.is_authenticated:
        return redirect('reports:dashboard')
    return render(request, 'accounts/home.html')


@role_required('admin')
def register_view(request):
    form = UserRegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('accounts:register')

    return render(request, 'accounts/register.html', {'form': form})
