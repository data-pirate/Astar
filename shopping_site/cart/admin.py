from django.contrib import admin
from .models import Cart, CartItem

# Register your models here.
class CartAdmin(admin.ModelAdmin):
    class meta:
        model = Cart

admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem)