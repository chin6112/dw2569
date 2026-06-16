import base64
from django.shortcuts import render
from rest_framework import viewsets
from .models import Order
from .serializers import OrderSerializer
from warehouse.models import Product

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('-created_at')
    serializer_class = OrderSerializer


def generate_placeholder_products(count):
    sample = [
        {'name': 'เครื่องซักผ้าอัจฉริยะ', 'sku': 'AP-001', 'stock': 200},
        {'name': 'ตู้เย็น 2 ประตู', 'sku': 'AP-002', 'stock': 150},
        {'name': 'ไมโครเวฟดิจิทัล', 'sku': 'AP-003', 'stock': 90},
        {'name': 'เครื่องกรองอากาศ', 'sku': 'AP-004', 'stock': 120},
        {'name': 'เครื่องปั่นผลไม้', 'sku': 'AP-005', 'stock': 80},
        {'name': 'ทีวี 4K 55 นิ้ว', 'sku': 'AP-006', 'stock': 60},
    ]
    items = []
    for idx in range(count):
        base = sample[idx % len(sample)]
        label = f"{base['name']} #{idx + 1}"
        svg = (
            '<svg xmlns="http://www.w3.org/2000/svg" width="420" height="280">'
            '<rect width="100%" height="100%" fill="#eef2f5"/>'
            '<text x="50%" y="38%" dominant-baseline="middle" text-anchor="middle" '
            'font-size="24" fill="#1a1a1a">เครื่องใช้ไฟฟ้า</text>'
            f'<text x="50%" y="58%" dominant-baseline="middle" text-anchor="middle" '
            f'font-size="18" fill="#555">{label}</text>'
            '<text x="50%" y="78%" dominant-baseline="middle" text-anchor="middle" '
            'font-size="14" fill="#888">Velvet Mart</text>'
            '</svg>'
        )
        encoded = base64.b64encode(svg.encode('utf-8')).decode('ascii')
        items.append({
            'name': base['name'],
            'sku': f"{base['sku']}-{idx + 1:02d}",
            'stock': base['stock'],
            'image_url': f'data:image/svg+xml;base64,{encoded}',
        })
    return items


def sales_home(request):
    categories = [
        {'name': 'เครื่องใช้ไฟฟ้า', 'subtitle': 'ตู้เย็น เตาอบ เครื่องซักผ้า'},
        {'name': 'ครัวสมัยใหม่', 'subtitle': 'หม้อหุงข้าว เครื่องปิ้งขนมปัง '} ,
        {'name': 'เครื่องกรองอากาศ', 'subtitle': 'พัดลม แอร์ และเครื่องฟอก'},
        {'name': 'เครื่องใช้ในบ้าน', 'subtitle': 'เครื่องดูดฝุ่น ไดร์เป่าผม'},
        {'name': 'เครื่องเสียง', 'subtitle': 'ทีวี ลำโพง และโฮมเธียเตอร์'},
    ]
    featured_products = list(Product.objects.filter(stock__gt=0).order_by('-stock')[:6])
    products = list(Product.objects.filter(stock__gt=0).order_by('-id')[:24])

    if not featured_products:
        featured_products = generate_placeholder_products(6)
    if not products:
        products = generate_placeholder_products(24)

    return render(request, 'webstore/sales.html', {
        'categories': categories,
        'featured_products': featured_products,
        'products': products,
    })
