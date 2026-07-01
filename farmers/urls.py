from django.urls import path

from . import views

app_name = 'farmers'

urlpatterns = [
    path('', views.farmer_list, name='list'),
    path('add/', views.farmer_create, name='create'),
    path('<int:pk>/', views.farmer_detail, name='detail'),
    path('<int:pk>/edit/', views.farmer_edit, name='edit'),
    path('centers/', views.center_list, name='centers'),
    path('centers/add/', views.center_create, name='center_create'),
]
