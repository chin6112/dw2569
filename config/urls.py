from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from webstore.views import sales_home
from warehouse.views import inventory_home
from marketing.views import marketing_home
from transport.views import transportation_home

urlpatterns = [
    path('', RedirectView.as_view(url='/sales/', permanent=False)),
    path('admin/', admin.site.urls),
    path('api/webstore/', include('webstore.urls')),
    path('sales/', sales_home),
    path('inventory/', inventory_home),
    path('marketing/', marketing_home),
    path('transportation/', transportation_home),
    path('api/warehouse/', include('warehouse.urls')),
    path('api/marketing/', include('marketing.urls')),
    path('api/transport/', include('transport.urls')),
]
