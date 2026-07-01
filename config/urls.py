from django.contrib import admin
from django.urls import include, path

from accounts import views as accounts_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', accounts_views.home_view, name='home'),
    path('accounts/', include('accounts.urls')),
    path('reports/', include('reports.urls')),
    path('farmers/', include('farmers.urls')),
    path('collection/', include('collection.urls')),
    path('billing/', include('billing.urls')),
]

admin.site.site_header = 'Online Milk Diary Admin'
admin.site.site_title = 'Milk Diary'
admin.site.index_title = 'Dairy Management Panel'
