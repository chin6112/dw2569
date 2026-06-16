from django.db import models

class Shipment(models.Model):
    tracking_number = models.CharField(max_length=100, unique=True)
    order_reference = models.CharField(max_length=100)
    carrier = models.CharField(max_length=255)
    status = models.CharField(max_length=50, default='pending')
    shipped_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.tracking_number
