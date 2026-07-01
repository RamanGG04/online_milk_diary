from django.urls import path

from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('daily/', views.daily_report, name='daily'),
    path('farmer/<int:pk>/ledger/', views.farmer_ledger, name='farmer_ledger'),
    path('export/excel/', views.export_daily_excel, name='export_excel'),
    path('export/pdf/', views.export_daily_pdf, name='export_pdf'),
]
