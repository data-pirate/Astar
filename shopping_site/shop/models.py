from django.db import models

# Create your models here.
class Product(models.Model):
    STATUS_CHOICES = (
        ('instock', 'Instock'),
        ('out of stock', 'out of stock')
    )
    product_name = models.CharField(max_length=150)
    category = models.CharField(max_length=100, default='')
    sub_category = models.CharField(max_length=100, default='')
    price = models.DecimalField(max_digits=100, decimal_places=2 ,default=0)
    desc = models.CharField(max_length=200, default='', null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    instock = models.CharField(max_length=20, choices=STATUS_CHOICES, default='instock')

    def __str__(self):
        return self.product_name

    def get_absolute_url(self):
        return 'product/%d/%s' %(self.id, self.desc)

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='shop/product_images', default='')
    featured = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.product.product_name