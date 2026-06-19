from django.db import DatabaseError
from django.shortcuts import render
from rest_framework import viewsets
from .models import Shipment
from .serializers import ShipmentSerializer


def transportation_home(request):
    try:
        shipments = list(Shipment.objects.all().order_by('-shipped_at'))
    except DatabaseError:
        shipments = []

    if not shipments:
        shipments = [
            {'tracking_number': f'TRK2026{idx + 1:04d}', 'order_reference': f'ORDER-{1000 + idx}', 'carrier': 'ThaiExpress', 'status': status, 'shipped_at': f'2026-06-{10 + idx:02d} 10:00'}
            for idx, status in enumerate(['กำลังจัดส่ง', 'จัดส่งแล้ว', 'รอลงทะเบียน'])
        ]

    return render(request, 'transport/transportation.html', {
        'shipments': shipments,
    })


class ShipmentViewSet(viewsets.ModelViewSet):
    queryset = Shipment.objects.all().order_by('-shipped_at')
    serializer_class = ShipmentSerializer
