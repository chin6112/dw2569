import base64
from django.shortcuts import render
from django.utils import timezone
from rest_framework import viewsets
from .models import Product, InventoryEntry
from .serializers import ProductSerializer, InventoryEntrySerializer

SAMPLE_PRODUCTS = [
    {'name': 'เครื่องใช้ไฟฟ้าอัจฉริยะ', 'sku': 'AP-001', 'stock': 200},
    {'name': 'ตู้เย็น 2 ประตู', 'sku': 'AP-002', 'stock': 150},
    {'name': 'ไมโครเวฟดิจิทัล', 'sku': 'AP-003', 'stock': 90},
    {'name': 'เครื่องกรองอากาศ', 'sku': 'AP-004', 'stock': 120},
    {'name': 'เครื่องปั่นผลไม้', 'sku': 'AP-005', 'stock': 80},
    {'name': 'ทีวี 4K 55 นิ้ว', 'sku': 'AP-006', 'stock': 60},
]


def build_placeholder_image(label):
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" width="420" height="280">'
        '<rect width="100%" height="100%" fill="#eef2f5"/>'
        '<text x="50%" y="38%" dominant-baseline="middle" text-anchor="middle"'
        ' font-size="24" fill="#1a1a1a">คลังสินค้า</text>'
        f'<text x="50%" y="58%" dominant-baseline="middle" text-anchor="middle"'
        f' font-size="18" fill="#555">{label}</text>'
        '<text x="50%" y="78%" dominant-baseline="middle" text-anchor="middle"'
        ' font-size="14" fill="#888">Velvet Mart</text>'
        '</svg>'
    )
    return 'data:image/svg+xml;base64,' + base64.b64encode(svg.encode('utf-8')).decode('ascii')


def generate_placeholder_products(count):
    products = []
    for idx in range(count):
        base = SAMPLE_PRODUCTS[idx % len(SAMPLE_PRODUCTS)]
        products.append({
            'name': base['name'],
            'sku': f"{base['sku']}-{idx + 1:02d}",
            'stock': base['stock'],
            'image_url': build_placeholder_image(base['name']),
        })
    return products


def inventory_home(request):
    try:
        products = list(Product.objects.filter(stock__gte=0).order_by('sku'))
    except DatabaseError:
        products = []

    try:
        inventory_entries = list(InventoryEntry.objects.select_related('product').order_by('-updated_at'))
    except DatabaseError:
        inventory_entries = []

    if not products:
        products = generate_placeholder_products(8)

    if not inventory_entries:
        inventory_entries = [
            {
                'product': products[i % len(products)],
                'quantity': prod['stock'],
                'updated_at': timezone.now().strftime('%Y-%m-%d %H:%M'),
            }
            for i, prod in enumerate(products)
        ]

    return render(request, 'warehouse/inventory.html', {
        'products': products,
        'inventory_entries': inventory_entries,
    })


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('sku')
    serializer_class = ProductSerializer


class InventoryEntryViewSet(viewsets.ModelViewSet):
    queryset = InventoryEntry.objects.all().order_by('-updated_at')
    serializer_class = InventoryEntrySerializer
