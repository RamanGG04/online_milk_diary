from django.contrib import messages
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import role_required
from collection.forms import MilkEntryForm, RateChartForm
from collection.models import MilkEntry, RateChart


@role_required('admin', 'operator', 'accountant')
def entry_list(request):
    date_filter = request.GET.get('date', '')
    entries = MilkEntry.objects.select_related('farmer', 'entered_by').all()
    if date_filter:
        entries = entries.filter(date=date_filter)

    summary = entries.aggregate(
        total_liters=Sum('quantity_liters'),
        total_amount=Sum('total_amount'),
    )
    return render(
        request,
        'collection/entry_list.html',
        {'entries': entries[:200], 'date_filter': date_filter, 'summary': summary},
    )


@role_required('admin', 'operator')
def entry_create(request):
    form = MilkEntryForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        entry = form.save(commit=False)
        entry.entered_by = request.user
        entry.save()
        messages.success(request, 'Milk entry saved successfully.')
        return redirect('collection:list')
    return render(request, 'collection/entry_form.html', {'form': form, 'title': 'Add Milk Entry'})


@role_required('admin', 'operator')
def entry_edit(request, pk):
    entry = get_object_or_404(MilkEntry, pk=pk)
    form = MilkEntryForm(request.POST or None, instance=entry)
    if request.method == 'POST' and form.is_valid():
        updated = form.save(commit=False)
        updated.entered_by = request.user
        updated.save()
        messages.success(request, 'Milk entry updated.')
        return redirect('collection:list')
    return render(request, 'collection/entry_form.html', {'form': form, 'title': 'Edit Milk Entry'})


@role_required('admin')
def rate_list(request):
    rates = RateChart.objects.all()
    return render(request, 'collection/rate_list.html', {'rates': rates})


@role_required('admin')
def rate_create(request):
    form = RateChartForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Rate chart entry added.')
        return redirect('collection:rates')
    return render(request, 'collection/rate_form.html', {'form': form, 'title': 'Add Rate'})
