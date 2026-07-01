from django.urls import path

from . import views

app_name = 'collection'

urlpatterns = [
    path('', views.entry_list, name='list'),
    path('add/', views.entry_create, name='create'),
    path('<int:pk>/edit/', views.entry_edit, name='edit'),
    path('rates/', views.rate_list, name='rates'),
    path('rates/add/', views.rate_create, name='rate_create'),
]
