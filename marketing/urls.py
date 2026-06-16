from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomerViewSet, CampaignViewSet

router = DefaultRouter()
router.register(r'customers', CustomerViewSet, basename='customer')
router.register(r'campaigns', CampaignViewSet, basename='campaign')

urlpatterns = [
    path('', include(router.urls)),
]
