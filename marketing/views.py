from rest_framework import viewsets
from .models import Customer, Campaign
from .serializers import CustomerSerializer, CampaignSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all().order_by('customer_code')
    serializer_class = CustomerSerializer

class CampaignViewSet(viewsets.ModelViewSet):
    queryset = Campaign.objects.all().order_by('-start_date')
    serializer_class = CampaignSerializer
