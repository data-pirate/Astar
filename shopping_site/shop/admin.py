from django.contrib import admin
from .models import Product, ProductImage


# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    search_fields = ['product_name', 'desc']
    list_display = ['product_name','category','price','date', 'instock']
    list_editable = ['price','instock']
    list_filter = ['price']
    prepopulated_fields = {'desc':('product_name',)}
    class meta:
        model = Product

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)