from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from webstore.views import sales_home

urlpatterns = [
    path('', RedirectView.as_view(url='/sales/', permanent=False)),
    path('admin/', admin.site.urls),
    path('api/webstore/', include('webstore.urls')),
    path('sales/', sales_home),
    path('api/warehouse/', include('warehouse.urls')),
    path('api/marketing/', include('marketing.urls')),
    path('api/transport/', include('transport.urls')),
]
