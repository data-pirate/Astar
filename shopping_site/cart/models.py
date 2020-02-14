from shop.models import Product
from django.db import models

# Create your models here.


class Cart(models.Model):
    products = models.ManyToManyField(Product, blank=True)
    total = models.DecimalField(max_digits=1000, decimal_places=2, default=0.00)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.id)
