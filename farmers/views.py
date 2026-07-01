from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import role_required
from farmers.forms import CollectionCenterForm, FarmerForm
from farmers.models import CollectionCenter, Farmer


@role_required('admin', 'operator', 'accountant')
def farmer_list(request):
    query = request.GET.get('q', '')
    farmers = Farmer.objects.select_related('center').all()
    if query:
        farmers = farmers.filter(
            Q(name__icontains=query) | Q(farmer_id__icontains=query) | Q(village__icontains=query)
        )
    return render(request, 'farmers/farmer_list.html', {'farmers': farmers, 'query': query})


@role_required('admin', 'operator')
def farmer_create(request):
    form = FarmerForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Farmer registered successfully.')
        return redirect('farmers:list')
    return render(request, 'farmers/farmer_form.html', {'form': form, 'title': 'Add Farmer'})


@role_required('admin', 'operator')
def farmer_edit(request, pk):
    farmer = get_object_or_404(Farmer, pk=pk)
    form = FarmerForm(request.POST or None, instance=farmer)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Farmer updated successfully.')
        return redirect('farmers:detail', pk=pk)
    return render(request, 'farmers/farmer_form.html', {'form': form, 'title': 'Edit Farmer'})


@role_required('admin', 'operator', 'accountant', 'farmer')
def farmer_detail(request, pk):
    farmer = get_object_or_404(Farmer, pk=pk)
    if request.user.is_farmer_user() and getattr(request.user, 'farmer_profile', None) != farmer:
        return redirect('reports:dashboard')
    entries = farmer.milk_entries.all()[:20]
    payments = farmer.payments.all()[:6]
    return render(
        request,
        'farmers/farmer_detail.html',
        {'farmer': farmer, 'entries': entries, 'payments': payments},
    )


@role_required('admin')
def center_list(request):
    centers = CollectionCenter.objects.all()
    return render(request, 'farmers/center_list.html', {'centers': centers})


@role_required('admin')
def center_create(request):
    form = CollectionCenterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Collection center added.')
        return redirect('farmers:centers')
    return render(request, 'farmers/center_form.html', {'form': form, 'title': 'Add Center'})
