from rest_framework import viewsets
from .models import Product, InventoryEntry
from .serializers import ProductSerializer, InventoryEntrySerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('sku')
    serializer_class = ProductSerializer

class InventoryEntryViewSet(viewsets.ModelViewSet):
    queryset = InventoryEntry.objects.all().order_by('-updated_at')
    serializer_class = InventoryEntrySerializer
