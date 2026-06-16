from django.db import models

class Customer(models.Model):
    customer_code = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    segment = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.customer_code

class Campaign(models.Model):
    name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    budget = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return self.name
