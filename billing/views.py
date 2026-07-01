from datetime import date
from decimal import Decimal

from django.contrib import messages
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import role_required
from billing.forms import DeductionForm, PaymentForm
from billing.models import Deduction, Payment
from collection.models import MilkEntry
from farmers.models import Farmer


def _month_start(value):
    if isinstance(value, date):
        return value.replace(day=1)
    return date.today().replace(day=1)


@role_required('admin', 'accountant')
def payment_list(request):
    month = request.GET.get('month')
    payments = Payment.objects.select_related('farmer').all()
    if month:
        payments = payments.filter(month=month)
    return render(request, 'billing/payment_list.html', {'payments': payments, 'month': month})


@role_required('admin', 'accountant')
def generate_payments(request):
    month_str = request.GET.get('month') or request.POST.get('month')
    if month_str:
        year, month = map(int, month_str.split('-'))
        month_date = date(year, month, 1)
    else:
        month_date = date.today().replace(day=1)

    if request.method == 'POST':
        farmers = Farmer.objects.filter(is_active=True)
        created = 0
        for farmer in farmers:
            entries = MilkEntry.objects.filter(
                farmer=farmer,
                date__year=month_date.year,
                date__month=month_date.month,
            )
            totals = entries.aggregate(
                liters=Sum('quantity_liters'),
                amount=Sum('total_amount'),
            )
            liters = totals['liters'] or Decimal('0')
            gross = totals['amount'] or Decimal('0')
            deductions = Deduction.objects.filter(
                farmer=farmer,
                month__year=month_date.year,
                month__month=month_date.month,
            ).aggregate(total=Sum('amount'))['total'] or Decimal('0')
            net = gross - deductions

            payment, was_created = Payment.objects.update_or_create(
                farmer=farmer,
                month=month_date,
                defaults={
                    'total_liters': liters,
                    'gross_amount': gross,
                    'total_deductions': deductions,
                    'net_amount': net,
                },
            )
            if was_created:
                created += 1

        messages.success(request, f'Monthly billing generated/updated for {month_date.strftime("%B %Y")}.')
        return redirect('billing:payments')

    return render(request, 'billing/generate_payments.html', {'month_date': month_date})


@role_required('admin', 'accountant')
def payment_edit(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    form = PaymentForm(request.POST or None, instance=payment)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Payment updated.')
        return redirect('billing:payments')
    return render(request, 'billing/payment_form.html', {'form': form, 'payment': payment})


@role_required('admin', 'accountant')
def deduction_list(request):
    deductions = Deduction.objects.select_related('farmer').all()
    return render(request, 'billing/deduction_list.html', {'deductions': deductions})


@role_required('admin', 'accountant')
def deduction_create(request):
    form = DeductionForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        deduction = form.save(commit=False)
        deduction.month = _month_start(deduction.month)
        deduction.save()
        messages.success(request, 'Deduction added.')
        return redirect('billing:deductions')
    return render(request, 'billing/deduction_form.html', {'form': form, 'title': 'Add Deduction'})
