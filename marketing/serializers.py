from rest_framework import serializers
from .models import Customer, Campaign

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'customer_code', 'name', 'email', 'phone', 'segment']

class CampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = ['id', 'name', 'start_date', 'end_date', 'budget']
