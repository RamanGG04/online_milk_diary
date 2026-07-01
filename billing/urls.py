from django.urls import path

from . import views

app_name = 'billing'

urlpatterns = [
    path('payments/', views.payment_list, name='payments'),
    path('payments/generate/', views.generate_payments, name='generate'),
    path('payments/<int:pk>/edit/', views.payment_edit, name='payment_edit'),
    path('deductions/', views.deduction_list, name='deductions'),
    path('deductions/add/', views.deduction_create, name='deduction_create'),
]
