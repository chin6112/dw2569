from rest_framework import serializers
from .models import Shipment

class ShipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipment
        fields = ['id', 'tracking_number', 'order_reference', 'carrier', 'status', 'shipped_at']
