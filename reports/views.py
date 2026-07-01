import json
from datetime import date, timedelta
from io import BytesIO

from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from openpyxl import Workbook
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from billing.models import Payment
from collection.models import MilkEntry
from farmers.models import Farmer


@login_required
def dashboard(request):
    user = request.user
    today = date.today()
    month_start = today.replace(day=1)

    if user.is_farmer_user() and hasattr(user, 'farmer_profile'):
        farmer = user.farmer_profile
        entries = MilkEntry.objects.filter(farmer=farmer)
        context = {
            'role': 'farmer',
            'farmer': farmer,
            'today_liters': entries.filter(date=today).aggregate(Sum('quantity_liters'))['quantity_liters__sum'] or 0,
            'month_liters': entries.filter(date__gte=month_start).aggregate(Sum('quantity_liters'))['quantity_liters__sum'] or 0,
            'month_amount': entries.filter(date__gte=month_start).aggregate(Sum('total_amount'))['total_amount__sum'] or 0,
            'recent_entries': entries[:10],
            'recent_payments': farmer.payments.all()[:5],
        }
        return render(request, 'reports/dashboard.html', context)

    today_stats = MilkEntry.objects.filter(date=today).aggregate(
        liters=Sum('quantity_liters'),
        amount=Sum('total_amount'),
        farmers=Count('farmer', distinct=True),
    )
    month_stats = MilkEntry.objects.filter(date__gte=month_start).aggregate(
        liters=Sum('quantity_liters'),
        amount=Sum('total_amount'),
    )
    pending_payments = Payment.objects.filter(status='pending').count()
    active_farmers = Farmer.objects.filter(is_active=True).count()
    recent_entries = MilkEntry.objects.select_related('farmer').order_by('-created_at')[:8]

    last_7_days = []
    for i in range(6, -1, -1):
        d = today - timedelta(days=i)
        day_total = MilkEntry.objects.filter(date=d).aggregate(Sum('quantity_liters'))['quantity_liters__sum'] or 0
        last_7_days.append({'date': d.strftime('%d %b'), 'liters': float(day_total)})

    context = {
        'role': 'staff',
        'today_stats': today_stats,
        'month_stats': month_stats,
        'pending_payments': pending_payments,
        'active_farmers': active_farmers,
        'recent_entries': recent_entries,
        'chart_labels': json.dumps([d['date'] for d in last_7_days]),
        'chart_data': json.dumps([d['liters'] for d in last_7_days]),
    }
    return render(request, 'reports/dashboard.html', context)


@login_required
def daily_report(request):
    report_date = request.GET.get('date', str(date.today()))
    entries = MilkEntry.objects.filter(date=report_date).select_related('farmer', 'farmer__center')
    summary = entries.aggregate(
        total_liters=Sum('quantity_liters'),
        total_amount=Sum('total_amount'),
        farmer_count=Count('farmer', distinct=True),
    )
    return render(
        request,
        'reports/daily_report.html',
        {'entries': entries, 'report_date': report_date, 'summary': summary},
    )


@login_required
def farmer_ledger(request, pk):
    farmer = get_object_or_404(Farmer, pk=pk)
    if request.user.is_farmer_user() and getattr(request.user, 'farmer_profile', None) != farmer:
        return redirect('reports:dashboard')

    month = request.GET.get('month')
    entries = farmer.milk_entries.all()
    if month:
        year, mon = map(int, month.split('-'))
        entries = entries.filter(date__year=year, date__month=mon)

    totals = entries.aggregate(
        liters=Sum('quantity_liters'),
        amount=Sum('total_amount'),
    )
    return render(
        request,
        'reports/farmer_ledger.html',
        {'farmer': farmer, 'entries': entries, 'totals': totals, 'month': month},
    )


@login_required
def export_daily_excel(request):
    report_date = request.GET.get('date', str(date.today()))
    entries = MilkEntry.objects.filter(date=report_date).select_related('farmer')

    wb = Workbook()
    ws = wb.active
    ws.title = 'Daily Collection'
    ws.append(['Farmer ID', 'Name', 'Shift', 'Liters', 'Fat %', 'SNF %', 'Rate', 'Amount'])
    for e in entries:
        ws.append([
            e.farmer.farmer_id, e.farmer.name, e.get_shift_display(),
            float(e.quantity_liters), float(e.fat_percent), float(e.snf_percent),
            float(e.rate_per_liter), float(e.total_amount),
        ])

    output = BytesIO()
    wb.save(output)
    output.seek(0)
    response = HttpResponse(
        output.read(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = f'attachment; filename=daily_report_{report_date}.xlsx'
    return response


@login_required
def export_daily_pdf(request):
    report_date = request.GET.get('date', str(date.today()))
    entries = MilkEntry.objects.filter(date=report_date).select_related('farmer')

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(A4))
    styles = getSampleStyleSheet()
    elements = [
        Paragraph(f'<b>Daily Milk Collection Report - {report_date}</b>', styles['Title']),
        Spacer(1, 12),
    ]

    data = [['Farmer ID', 'Name', 'Shift', 'Liters', 'Fat %', 'Amount']]
    total_liters = 0
    total_amount = 0
    for e in entries:
        data.append([
            e.farmer.farmer_id, e.farmer.name, e.get_shift_display(),
            str(e.quantity_liters), str(e.fat_percent), str(e.total_amount),
        ])
        total_liters += float(e.quantity_liters)
        total_amount += float(e.total_amount)
    data.append(['', '', 'TOTAL', f'{total_liters:.2f}', '', f'{total_amount:.2f}'])

    table = Table(data, repeatRows=1)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0d6efd')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#e9ecef')),
    ]))
    elements.append(table)
    doc.build(elements)

    buffer.seek(0)
    response = HttpResponse(buffer.read(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=daily_report_{report_date}.pdf'
    return response
