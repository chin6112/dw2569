import base64
from django.db import models

class Product(models.Model):
    sku = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    stock = models.IntegerField(default=0)
    location = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.sku

    @property
    def image_url(self):
        label = self.name or self.sku
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
        return f'data:image/svg+xml;base64,{encoded}'

class InventoryEntry(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='inventory_entries')
    quantity = models.IntegerField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.product.sku} - {self.quantity}'
