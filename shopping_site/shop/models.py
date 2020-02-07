from django.db import models

# Create your models here.
class Product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=150)
    category = models.CharField(max_length=100, default='')
    sub_category = models.CharField(max_length=100, default='')
    price = models.FloatField(default=0)
    desc = models.CharField(max_length=200, default='')
    date = models.DateField()
    image = models.ImageField(upload_to='shop/product_images', default='')


    def __str__(self):
        return self.product_name