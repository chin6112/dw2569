from django.db import DatabaseError
from django.shortcuts import render
from rest_framework import viewsets
from .models import Customer, Campaign
from .serializers import CustomerSerializer, CampaignSerializer


def marketing_home(request):
    try:
        customers = list(Customer.objects.all().order_by('customer_code'))
    except DatabaseError:
        customers = []

    try:
        campaigns = list(Campaign.objects.all().order_by('-start_date'))
    except DatabaseError:
        campaigns = []

    if not customers:
        customers = [
            {'customer_code': f'CUST-{idx + 1:03d}', 'name': name, 'email': f'customer{idx + 1}@example.com', 'phone': f'080-0000{idx + 1:02d}', 'segment': segment}
            for idx, (name, segment) in enumerate([
                ('บริษัท ต้นไม้ จำกัด', 'VIP'),
                ('ร้านอาหารสุขใจ', 'SME'),
                ('คลินิกสุขภาพดี', 'Corporate'),
            ])
        ]

    if not campaigns:
        campaigns = [
            {'name': 'โปรโมชันหน้าร้อน', 'start_date': '2026-06-01', 'end_date': '2026-06-30', 'budget': '150000.00'},
            {'name': 'แจกโค้ดส่วนลด', 'start_date': '2026-07-01', 'end_date': '2026-07-15', 'budget': '75000.00'},
        ]

    return render(request, 'marketing/marketing.html', {
        'customers': customers,
        'campaigns': campaigns,
    })


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all().order_by('customer_code')
    serializer_class = CustomerSerializer


class CampaignViewSet(viewsets.ModelViewSet):
    queryset = Campaign.objects.all().order_by('-start_date')
    serializer_class = CampaignSerializer
